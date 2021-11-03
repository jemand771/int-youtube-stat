import unittest
from api_helper import YouTubeApi, InvalidLinkFormatException


class YtApiTest(unittest.TestCase):
    TEST_PLAYLIST = 'https://www.youtube.com/playlist?list=PLRktPAG0Z4OYxnRWDJphPh11euBWSMucb'

    def setUp(self) -> None:
        self.api = YouTubeApi()

    def test_get_video_via_multiple_success(self):
        rick_roll_data = self.api.get_video_data_multi(['dQw4w9WgXcQ'])
        self.assertEqual(rick_roll_data[0].title, 'Rick Astley - Never Gonna Give You Up (Official Music Video)')
        self.assertEqual(rick_roll_data[0].id, 'dQw4w9WgXcQ')

    def test_get_video_ids_success(self):
        video_ids = self.api.get_video_ids_from_link(self.TEST_PLAYLIST)
        # just check some carefully chosen videos from this playlist
        self.assertIn('KtJ79ZjJ3lM', video_ids)
        self.assertIn('l-Egisu_4AA', video_ids)
        self.assertIn('l77qrAnW1N4', video_ids)

    def test_get_video_ids_fail_link_format(self):
        self.assertRaises(InvalidLinkFormatException, self.api.get_video_ids_from_link, 'some shit but no URL')

    def test_get_stats_success(self):
        stats = self.api.get_stats(self.api.get_video_ids_from_link(self.TEST_PLAYLIST))
        self.assertIsNone(stats)  # TODO fill when stats are implemented
