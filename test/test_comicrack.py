import json
import os
import tempfile
import unittest
from unittest.mock import patch, MagicMock
import xml.etree.ElementTree as ET

from bdnex.lib.comicrack import comicInfo

TEST_ROOT = os.path.dirname(__file__)
ARCHIVE_CBZ_PATH = os.path.join(TEST_ROOT, 'bd.cbz')


class TestComicInfo(unittest.TestCase):
    def setUp(self):
        self.sample_comic_info = {
            "ComicInfo": {
                "Title": "Test Comic",
                "Series": "Test Series",
                "Number": "1",
                "Summary": "A test comic book",
                "Writer": "Test Writer",
                "Penciller": "Test Artist",
                "Publisher": "Test Publisher",
                "Genre": "Adventure",
                "Web": "https://example.com",
                "CommunityRating": 4.5
            }
        }

    def test_comicInfo_xml_create(self):
        """Test that ComicInfo XML is created correctly"""
        comic = comicInfo(comic_info=self.sample_comic_info)
        comic_info_fp = comic.comicInfo_xml_create()

        # Check that file was created
        self.assertTrue(os.path.exists(comic_info_fp))
        self.assertEqual('ComicInfo.xml', os.path.basename(comic_info_fp))

        # Check XML structure
        tree = ET.parse(comic_info_fp)
        root = tree.getroot()
        self.assertEqual('ComicInfo', root.tag)

        # Verify some elements exist
        title = root.find('Title')
        self.assertIsNotNone(title)
        self.assertEqual("Test Comic", title.text)

        series = root.find('Series')
        self.assertIsNotNone(series)
        self.assertEqual("Test Series", series.text)

        # Cleanup
        os.remove(comic_info_fp)
        os.rmdir(os.path.dirname(comic_info_fp))

    def test_comicInfo_init(self):
        """Test comicInfo initialization"""
        comic = comicInfo(input_filename=ARCHIVE_CBZ_PATH, comic_info=self.sample_comic_info)
        self.assertEqual(ARCHIVE_CBZ_PATH, comic.input_filename)
        self.assertEqual(self.sample_comic_info, comic.comic_info)


if __name__ == '__main__':
    unittest.main()
