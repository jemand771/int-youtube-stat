import os
import unittest
from api_helper import YouTubeApi, InvalidLinkFormatException, VideoNotFoundException, YouTubeStatistics
import app as main_app

from parameterized import parameterized


class TestYtApiHelper(unittest.TestCase):
    TEST_PLAYLIST = 'https://www.youtube.com/playlist?list=PLRktPAG0Z4OYxnRWDJphPh11euBWSMucb'
    TEST_LONG_VIDEO = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
    TEST_SHORT_VIDEO = 'https://youtu.be/dQw4w9WgXcQ'
    TEST_RR_ID = 'dQw4w9WgXcQ'

    def setUp(self) -> None:
        self.api = YouTubeApi(os.environ.get("YOUTUBE_API_TEST_KEY"), False)

    def tearDown(self) -> None:
        # fix ResourceWarning from unittest x open requests session
        self.api.api.session.close()

    def test_get_video_data_via_multiple_success(self):
        rick_roll_data = self.api.get_video_data_multi([self.TEST_RR_ID])
        self.assertEqual(rick_roll_data[0].title, 'Rick Astley - Never Gonna Give You Up (Official Music Video)')
        self.assertEqual(rick_roll_data[0].id, self.TEST_RR_ID)

    def test_get_video_data_invalid_id(self):
        self.assertRaises(VideoNotFoundException, self.api.get_video_data, 'noid')

    def test_get_video_ids_success_playlist_success(self):
        video_ids = self.api.get_video_ids_from_link(self.TEST_PLAYLIST)
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


class TestHttpApi(unittest.TestCase):

    def setUp(self) -> None:
        self.api = YouTubeApi(os.environ.get("YOUTUBE_API_TEST_KEY"), False)
        self.app = main_app.app.test_client()

    def tearDown(self) -> None:
        # fix ResourceWarning from unittest x open requests session
        self.api.api.session.close()

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
            self.api.get_video_data_multi(
                self.api.get_video_ids_from_link(
                    video_url
                )
            )[0].title
        )

    def test_stats(self):
        r = self.app.post("/stats", json=[TestYtApiHelper.TEST_RR_ID] * 3)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(
            YouTubeStatistics(**r.json),
            self.api.get_stats([TestYtApiHelper.TEST_RR_ID] * 3)
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

