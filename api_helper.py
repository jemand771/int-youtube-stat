import os
from dataclasses import dataclass
import functools
import shelve
import time
import urllib.parse

import pyyoutube


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


def cached(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # args[0] will be self for decorated instance methods
        cache_config = args[0].cache_config
        if not cache_config:
            return func(*args, **kwargs)
        # this is hacky but.. don't @ me
        cache_key = str((func.__name__, args[1:], tuple(kwargs.items())))
        with shelve.open(cache_config["file"]) as cache:
            cache_obj = cache.get(cache_key)
            if cache_obj:
                if cache_obj["time"] + cache_config["time"] > time.time():
                    return cache_obj["value"]
                cache.pop(cache_key)
            val = func(*args, **kwargs)
            cache[cache_key] = {
                "time": int(time.time()),
                "value": val
            }
            return val
    return wrapper


class YouTubeApi:

    def __init__(self, api_key=None, use_cache=True, cache_file=".cache.shelve", cache_time=900):
        if api_key:
            self.api = pyyoutube.Api(api_key=api_key)
        self.cache_config = {
            "file": cache_file,
            "time": cache_time
        } if use_cache else None

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
    api = YouTubeApi(os.environ.get("YOUTUBE_API_KEY"))
    ids = api.get_video_ids_from_link("https://www.youtube.com/playlist?list=PLRktPAG0Z4OYxnRWDJphPh11euBWSMucb")
    for video_id_ in ids:
        print(api.get_video_data(video_id_))
