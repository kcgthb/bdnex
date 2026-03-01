import os
import sys
import unittest
from unittest.mock import patch
from bdnex.lib.utils import bdnex_config, yesno, enter_album_url, _init_config


class TestUtils(unittest.TestCase):

    @patch('bdnex.lib.utils._init_config')
    def test_bdnex_config(self, _init_config_mock):
        _init_config_mock.return_value = os.path.join(os.path.join(os.path.dirname(__file__), "bdnex.yaml"))
        conf = bdnex_config()
        self.assertTrue('bdnex' in conf)

    @patch('builtins.input', side_effect=['nooooo', 'Y'])
    def test_yesno(self, input):
        self.assertTrue(yesno('do you need this? Y/N'))

    @patch('builtins.input', side_effect=['nooooo', 'def nop', 'i give up', 'n'])
    def test_yesno(self, input):
        self.assertFalse(yesno('do you need this? Y/N'))

    @patch('builtins.input', side_effect=['a', 'b', 'c', 'https://www.bedetheque.com/nain.html'])
    def test_enter_album_url(self, input):
        self.assertEqual('https://m.bedetheque.com/nain.html', enter_album_url())

    @patch('builtins.input', side_effect=['a', 'b', 'https://www.bedetheque.com/nain.html'])
    def test_enter_album_url(self, input):
        self.assertEqual('https://m.bedetheque.com/nain.html', enter_album_url())

    @patch('bdnex.lib.utils.shutil.copy')
    @patch('bdnex.lib.utils.os.makedirs')
    @patch('bdnex.lib.utils.os.path.exists', return_value=True)
    @patch.dict('os.environ', {'XDG_CONFIG_HOME': '/custom/xdg'}, clear=False)
    @patch('bdnex.lib.utils.sys.platform', 'linux')
    def test_init_config_linux_xdg(self, mock_exists, mock_makedirs, mock_copy):
        path = _init_config()
        self.assertTrue(path.startswith('/custom/xdg'))
        self.assertTrue(path.endswith('bdnex.yaml'))
        mock_makedirs.assert_not_called()
        mock_copy.assert_not_called()

    @patch('bdnex.lib.utils.shutil.copy')
    @patch('bdnex.lib.utils.os.makedirs')
    @patch('bdnex.lib.utils.os.path.exists', return_value=True)
    @patch.dict('os.environ', {}, clear=True)
    @patch('bdnex.lib.utils.sys.platform', 'linux')
    def test_init_config_linux_fallback(self, mock_exists, mock_makedirs, mock_copy):
        path = _init_config()
        expected_base = os.path.expanduser('~/.config')
        self.assertTrue(path.startswith(expected_base))
        self.assertTrue(path.endswith('bdnex.yaml'))

    @patch('bdnex.lib.utils.shutil.copy')
    @patch('bdnex.lib.utils.os.makedirs')
    @patch('bdnex.lib.utils.os.path.exists', return_value=False)
    @patch.dict('os.environ', {'APPDATA': 'C:\\Users\\test\\AppData\\Roaming'}, clear=False)
    @patch('bdnex.lib.utils.sys.platform', 'win32')
    def test_init_config_windows(self, mock_exists, mock_makedirs, mock_copy):
        path = _init_config()
        self.assertTrue(path.startswith('C:\\Users\\test\\AppData\\Roaming'))
        self.assertTrue(path.endswith('bdnex.yaml'))
        mock_makedirs.assert_called_once()
        mock_copy.assert_called_once()

    @patch('bdnex.lib.utils.shutil.copy')
    @patch('bdnex.lib.utils.os.makedirs')
    @patch('bdnex.lib.utils.os.path.exists', side_effect=[False, False])
    @patch.dict('os.environ', {'XDG_CONFIG_HOME': '/xdg'}, clear=False)
    @patch('bdnex.lib.utils.sys.platform', 'linux')
    def test_init_config_creates_dir_and_copies_default(self, mock_exists, mock_makedirs, mock_copy):
        path = _init_config()
        mock_makedirs.assert_called_once()
        mock_copy.assert_called_once()
        self.assertTrue(path.endswith('bdnex.yaml'))
