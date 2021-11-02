from dataclasses import dataclass
import functools
import os
import shelve
import time
import urllib.parse

import pyyoutube


# TODO make this configurable via env variables?
SHELVE_FILE = ".cache.shelve"
CACHE_TIME = 10


class InvalidLinkFormatException(ValueError):
    pass


@dataclass
class YouTubeVideo:
    id: str
    title: str
    duration: int
    thumbnail_url: str


@dataclass
class YouTubeStatistics:
    pass


class YouTubeApi:

    def cached(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            # this is hacky but.. don't @ me
            cache_key = str((func.__name__, args, tuple(kwargs.items())))
            with shelve.open(SHELVE_FILE) as cache:
                cache_obj = cache.get(cache_key)
                if cache_obj:
                    if cache_obj["time"] + CACHE_TIME > time.time():
                        return cache_obj["value"]
                    cache.pop(cache_key)
                val = func(self, *args, **kwargs)
                cache[cache_key] = {
                    "time": int(time.time()),
                    "value": val
                }
                return val
        return wrapper

    # TODO implement local caching, use locking (!)

    def __init__(self):
        self.api = pyyoutube.Api(api_key=os.environ.get("YOUTUBE_API_KEY"))
        # TODO add a flag or env var 

    def _video_ids_from_playlist_id(self, playlist_id: str) -> list[str]:
        return [
            video.contentDetails.videoId
            for video
            in self.api.get_playlist_items(
                playlist_id=playlist_id,
                count=None,
                parts="contentDetails"
            ).items
        ]

    def get_video_ids_from_link(self, url: str) -> list[str]:
        # TODO more url matching :)
        #      evtl. auch einfach machbar für colin/franz?
        url_obj = urllib.parse.urlparse(url)
        # we're using parse_qsl instead of parse_qs because nobody cares about list-encoded query parameters
        query = dict(urllib.parse.parse_qsl(url_obj.query))
        if url_obj.netloc == "www.youtube.com":
            if url_obj.path == "/playlist":
                if query.get("list"):
                    return self._video_ids_from_playlist_id(query.get("list"))
        raise InvalidLinkFormatException("meh")

    @cached
    def get_video_data(self, video_id: str) -> YouTubeVideo:
        video = self.api.get_video_by_id(video_id=video_id).items[0]
        # get all possible thumbnail variants
        th_v = video.snippet.thumbnails
        # pick highest res thumbnail
        thumbnail = th_v.maxres or th_v.standard or th_v.high or th_v.medium or th_v.default
        return YouTubeVideo(
            id=video.id,
            title=video.snippet.title,
            duration=video.contentDetails.get_video_seconds_duration(),
            thumbnail_url=thumbnail.url,
        )

    def get_video_data_multi(self, video_ids: list[str]) -> list[YouTubeVideo]:
        return [self.get_video_data(video_id) for video_id in video_ids]

    def get_stats(self, video_ids: list[str]) -> YouTubeStatistics:
        pass  # TODO implement statistics accumulator


# TODO remove this part again
if __name__ == "__main__":
    print("hello world")
    api = YouTubeApi()
    # print(api.get_video_ids_from_link("https://www.youtube.com/playlist?list=PLRktPAG0Z4OYxnRWDJphPh11euBWSMucb"))
    print(api.get_video_data("QQrfPbDkIoE"))
