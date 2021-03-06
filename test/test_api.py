import os
import unittest
from api_helper import YouTubeApi, InvalidLinkFormatException, VideoNotFoundException, YouTubeVideo
import app as main_app

from parameterized import parameterized


class ApiTestBase(unittest.TestCase):
    def setUp(self) -> None:
        self.api = self.make_api()

    def tearDown(self) -> None:
        # fix ResourceWarning from unittest x open requests session
        self.api.api.session.close()

    @staticmethod
    def make_api(use_cache=False, **kwargs):
        return YouTubeApi(os.environ.get("YOUTUBE_API_TEST_KEY"), use_cache=use_cache, **kwargs)


class TestYtApiHelper(ApiTestBase):
    TEST_PLAYLIST = 'https://www.youtube.com/playlist?list=PLRktPAG0Z4OYxnRWDJphPh11euBWSMucb'
    TEST_LONG_VIDEO = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
    TEST_SHORT_VIDEO = 'https://youtu.be/dQw4w9WgXcQ'
    TEST_VIDEO_WITH_PLAYLIST = 'https://www.youtube.com/watch?v=KtJ79ZjJ3lM&list=PLRktPAG0Z4OYxnRWDJphPh11euBWSMucb&index=2'
    TEST_RR_ID = 'dQw4w9WgXcQ'
    TEST_LONG_DURATION_VIDEO_ID = 'jIQ6UV2onyI'

    def test_get_video_data_success(self):
        rick_roll_data = self.api.get_video_data(self.TEST_RR_ID)
        self.assertEqual(rick_roll_data.title, 'Rick Astley - Never Gonna Give You Up (Official Music Video)')
        self.assertEqual(rick_roll_data.id, self.TEST_RR_ID)

    def test_get_video_data_invalid_id(self):
        self.assertRaises(VideoNotFoundException, self.api.get_video_data, 'noid')

    def test_get_video_ids_success_playlist_success(self):
        video_ids = self.api.get_video_ids_from_link(self.TEST_PLAYLIST)
        # just check some carefully chosen videos from this playlist
        self.assertIn('KtJ79ZjJ3lM', video_ids)
        self.assertIn('l-Egisu_4AA', video_ids)
        self.assertIn('l77qrAnW1N4', video_ids)

    def test_get_video_ids_from_watch_link_with_list_success(self):
        video_ids = self.api.get_video_ids_from_link(self.TEST_VIDEO_WITH_PLAYLIST)
        # just check some carefully chosen videos from this playlist
        self.assertIn('KtJ79ZjJ3lM', video_ids)
        self.assertIn('l-Egisu_4AA', video_ids)
        self.assertIn('l77qrAnW1N4', video_ids)

    def test_get_video_id_from_video_link_success(self):
        rrid_short = self.api.get_video_ids_from_link(self.TEST_SHORT_VIDEO)
        rrid_long = self.api.get_video_ids_from_link(self.TEST_LONG_VIDEO)
        self.assertIn(self.TEST_RR_ID, rrid_short)
        self.assertIn(self.TEST_RR_ID, rrid_long)

    def test_get_video_ids_fail_link_format(self):
        self.assertRaises(InvalidLinkFormatException, self.api.get_video_ids_from_link, 'some shit but no URL')

    def test_get_stats_success(self):
        stats = self.api.get_stats(self.api.get_video_ids_from_link(self.TEST_PLAYLIST))
        # deckt nur den Fall ab, das neuer content zur Test-Playlist hinzu kommt
        self.assertGreaterEqual(stats.total_count, 24)
        self.assertGreaterEqual(stats.total_duration, 5773)


class TestHttpApi(ApiTestBase):

    def setUp(self) -> None:
        # overwrite the flask app's api object to use the testing key aswell
        main_app.api = self.make_api()
        self.app = main_app.app.test_client()
        super(TestHttpApi, self).setUp()

    def tearDown(self) -> None:
        main_app.api.api.session.close()
        super(TestHttpApi, self).tearDown()

    def test_not_found(self):
        r = self.app.get("/asdasd")
        self.assertEqual(r.status_code, 404)

    @parameterized.expand([
        ["short", TestYtApiHelper.TEST_SHORT_VIDEO],
        ["long", TestYtApiHelper.TEST_LONG_VIDEO]
    ])
    def test_video_info(self, _, video_url):
        r = self.app.get("/video_data/" + video_url)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(
            r.json[0].get("title"),
            self.api.get_video_data(
                self.api.get_video_ids_from_link(
                    video_url
                )[0]
            ).title
        )

    def test_stats(self):
        r = self.app.post("/stats", json=[TestYtApiHelper.TEST_RR_ID] * 3)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(
            r.json,
            main_app.MyJSONEncoder().default(
                self.api.get_stats([TestYtApiHelper.TEST_RR_ID] * 3)
            )
        )

    def test_home(self):
        r = self.app.get("/")
        self.assertEqual(r.status_code, 200)

    def test_invalid_url(self):
        r = self.app.get("/video_data/test")
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.data, b"invalid link")

    def test_invalid_stats_request_invalid_no_json(self):
        r = self.app.post("/stats")
        self.assertEqual(r.status_code, 400)

    def test_invalid_stats_request_invalid_json_type(self):
        r = self.app.post("/stats", json={"a": "b"})
        self.assertEqual(r.status_code, 400)

    def test_invalid_stats_request_invalid_json_content(self):
        r = self.app.post("/stats", json=["asdsad", 2, "asdasd"])
        self.assertEqual(r.status_code, 400)

    def test_formatter_hours_success(self):
        encoder = main_app.MyJSONEncoder()
        # while we could cast to TCount and TDuration here, we can also just let post_init handle that
        # noinspection PyTypeChecker
        r = encoder.default(YouTubeVideo(
            id="aaaaaaaaaaa",
            title="video title",
            duration=10 * 60 * 60 + 1,
            thumbnail_url="https://foo.bar",
            view_count=123,
            like_count=123_456_789,
            channel_id="some-id",
            channel_name="the best channel"
        ))
        self.assertEqual(r['duration'], '10:00:01')
        self.assertEqual(r['view_count'], '123')
        self.assertEqual(r['like_count'], '123,4Mio')
