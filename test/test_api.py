import os
import unittest
from api_helper import YouTubeApi, InvalidLinkFormatException, VideoNotFoundException


class TestYtApiHelper(unittest.TestCase):
    TEST_PLAYLIST = 'https://www.youtube.com/playlist?list=PLRktPAG0Z4OYxnRWDJphPh11euBWSMucb'
    TEST_LONG_VIDEO = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
    TEST_SHORT_VIDEO = 'https://youtu.be/dQw4w9WgXcQ'
    TEST_RR_ID = 'dQw4w9WgXcQ'

    def setUp(self) -> None:
        self.api = YouTubeApi(os.environ.get("YOUTUBE_API_KEY"), False)

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

    def test_being_slow(self):
        import time
        time.sleep(5)
    
    def test_failing(self):
        self.assertEqual(1, 2)
