import os
import unittest
from unittest.mock import patch

from bdnex.lib.cover import front_cover_similarity, get_bdgest_cover

TEST_ROOT = os.path.dirname(__file__)

BDGEST_COVER = os.path.join(TEST_ROOT, 'Couv_245127.jpg')
ARCHIVE_COVER = os.path.join(TEST_ROOT, 'Nains 1 00a.jpg')
BDGEST_OTHER_COVER = os.path.join(TEST_ROOT, 'Couv_272757.jpg')


class TestCover(unittest.TestCase):
    def test_front_cover_similarity(self):
        # check good cover similarity
        match_res = front_cover_similarity(ARCHIVE_COVER, BDGEST_COVER)
        self.assertEqual(True, match_res > 50)  #

        # check bad cover similarity
        match_res = front_cover_similarity(ARCHIVE_COVER, BDGEST_OTHER_COVER)
        self.assertEqual(True, match_res < 5)

    @patch('bdnex.lib.cover.bdnex_config')
    @patch('bdnex.lib.cover.os.path.exists')
    def test_get_bdgest_cover_uses_config_path(self, mock_exists, mock_bdnex_config):
        custom_share_path = '/custom/share/path'
        mock_bdnex_config.return_value = {'bdnex': {'share_path': custom_share_path}}
        expected_cover_path = os.path.join(custom_share_path, 'bedetheque/covers', 'Couv_12345.jpg')
        mock_exists.return_value = True

        result = get_bdgest_cover('https://www.bedetheque.com/media/Couvertures/Couv_12345.jpg')

        mock_exists.assert_called_once_with(expected_cover_path)
        self.assertEqual(expected_cover_path, result)


if __name__ == '__main__':
    unittest.main()
