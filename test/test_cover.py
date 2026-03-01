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


class TestGetBdgestCover(unittest.TestCase):
    def test_cover_path_uses_share_path_from_config(self):
        """Cover should be saved under share_path from bdnex_config, not HOME."""
        fake_config = {'bdnex': {'share_path': '/tmp/test_bdnex_share'}}
        cover_url = 'https://www.bedetheque.com/media/Couvertures/Couv_12345.jpg'
        expected_covers_dir = '/tmp/test_bdnex_share/bedetheque/covers'
        expected_cover_path = os.path.join(expected_covers_dir, 'Couv_12345.jpg')

        with patch('bdnex.lib.cover.bdnex_config', return_value=fake_config), \
             patch('bdnex.lib.cover.download_link', return_value=expected_cover_path) as mock_dl, \
             patch('os.path.exists', return_value=False):
            result = get_bdgest_cover(cover_url)

        mock_dl.assert_called_once_with(cover_url, expected_covers_dir)
        self.assertEqual(result, expected_cover_path)

    def test_cover_returns_cached_path_when_exists(self):
        """If the cover file already exists, it should be returned without downloading."""
        fake_config = {'bdnex': {'share_path': '/tmp/test_bdnex_share'}}
        cover_url = 'https://www.bedetheque.com/media/Couvertures/Couv_12345.jpg'
        expected_cover_path = '/tmp/test_bdnex_share/bedetheque/covers/Couv_12345.jpg'

        with patch('bdnex.lib.cover.bdnex_config', return_value=fake_config), \
             patch('bdnex.lib.cover.download_link') as mock_dl, \
             patch('os.path.exists', return_value=True):
            result = get_bdgest_cover(cover_url)

        mock_dl.assert_not_called()
        self.assertEqual(result, expected_cover_path)


if __name__ == '__main__':
    unittest.main()
