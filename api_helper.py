from dataclasses import dataclass
from datetime import timedelta
import functools
import math
import shelve
import time
import urllib.parse

import pyyoutube

TEXT_ERROR_NO_COUNT = "unknown"


class InvalidLinkFormatException(ValueError):
    def __init__(self, message):
        super().__init__(f"invalid link: {message}")


class VideoNotFoundException(ValueError):
    def __init__(self, message):
        super().__init__(f"video not found: {message}")


def format_count(num):
    # TODO test? -> <-
    magnitude = int(math.log10(num)) // 3
    num /= 10 ** (3 * magnitude)
    last_digit = int(10 * (num - int(num)))
    last_digit_fmt = f",{last_digit}" if last_digit else ""
    return f"{int(num)}{last_digit_fmt}{['', 'K', 'M', 'B', 'T'][magnitude]}"


class TCount(int):
    def __new__(cls, val):
        if val is None:
            val = -1
        return super(TCount, cls).__new__(cls, val)

    def __str__(self):
        if int(self) == -1:
            return TEXT_ERROR_NO_COUNT
        return format_count(int(self))


class TDuration(int):

    def __str__(self):
        total_seconds = int(self)
        seconds = total_seconds % 60
        total_seconds //= 60
        minutes = total_seconds % 60
        total_seconds //= 60
        hours = total_seconds
        format_str = f"{minutes:02}:{seconds:02}"
        if hours:
            format_str = f"{hours:02}:" + format_str
        return format_str


# common parent class for easier isinstance checks
class YouTubeData:
    pass


@dataclass
class YouTubeVideo(YouTubeData):
    id: str
    title: str
    duration: TDuration
    thumbnail_url: str
    view_count: TCount
    like_count: TCount
    channel_id: str
    channel_name: str


@dataclass
class YouTubeStatistics(YouTubeData):
    total_count: int
    total_duration: TDuration
    avg_duration: TDuration
    total_likes: TCount
    avg_likes: TCount
    total_views: TCount
    avg_views: TCount


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
        url_obj = urllib.parse.urlparse(url)
        # we're using parse_qsl instead of parse_qs because nobody cares about list-encoded query parameters
        query = dict(urllib.parse.parse_qsl(url_obj.query))
        if url_obj.netloc == "www.youtube.com" or url_obj.netloc == "youtube.com" or url_obj.netloc == "m.youtube.com":
            if url_obj.path == "/playlist":
                if query.get("list"):
                    return self._video_ids_from_playlist_id(query.get("list"))
            if url_obj.path == "/watch":  # TODO parse playlist IDs in watch links?
                if query.get("v"):
                    return [query.get("v")]
        elif url_obj.netloc == "youtu.be":
            return [url_obj.path[1:]]
        raise InvalidLinkFormatException("meh")

    @cached
    def get_video_data(self, video_id: str) -> YouTubeVideo:
        candidates = self.api.get_video_by_id(video_id=video_id).items
        if not candidates:
            raise VideoNotFoundException(video_id)
        video = candidates[0]
        # get all possible thumbnail variants
        th_v = video.snippet.thumbnails
        # pick highest res thumbnail
        thumbnail = th_v.maxres or th_v.standard or th_v.high or th_v.medium or th_v.default
        return YouTubeVideo(
            id=video.id,
            title=video.snippet.title,
            duration=TDuration(video.contentDetails.get_video_seconds_duration()),
            thumbnail_url=thumbnail.url,
            view_count=TCount(video.statistics.viewCount),
            like_count=TCount(video.statistics.likeCount),
            channel_name=video.snippet.channelTitle,
            channel_id=video.snippet.channelId
        )

    def get_video_data_multi(self, video_ids: list[str]) -> list[YouTubeVideo]:
        return [self.get_video_data(video_id) for video_id in video_ids]

    def get_stats(self, video_ids: list[str]) -> YouTubeStatistics:
        videos = [self.get_video_data(video_id) for video_id in video_ids]
        total_duration = sum(video.duration for video in videos)
        total_views = sum(video.view_count for video in videos)
        total_likes = sum(video.like_count for video in videos)
        # TODO I'm going to divide by zero here :^)
        # TODO refactor assignments? -> **
        # TODO remove need for TCount constructor?
        return YouTubeStatistics(
            total_count=len(videos),
            total_duration=TDuration(total_duration),
            avg_duration=TDuration(total_duration // len(videos)),
            total_likes=TCount(total_likes),
            avg_likes=TCount(total_likes // len(videos)),
            total_views=TCount(total_views),
            avg_views=TCount(total_views // len(videos))
        )
