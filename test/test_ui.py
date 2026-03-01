import sys
import unittest
from unittest.mock import patch, MagicMock

# Stub out modules not available in the test environment before importing bdnex.ui
for _mod in ('rarfile', 'bs4', 'termcolor', 'InquirerPy', 'InquirerPy.base.control',
             'InquirerPy.separator', 'PIL', 'PIL.Image', 'skimage', 'skimage.metrics',
             'pandas', 'lxml', 'lxml.etree', 'rapidfuzz', 'rapidfuzz.fuzz',
             'patoolib', 'xmlschema', 'xmldiff', 'cv2', 'imutils'):
    if _mod not in sys.modules:
        sys.modules[_mod] = MagicMock()

import bdnex.ui


class TestMain(unittest.TestCase):

    @patch('bdnex.ui.args')
    @patch('bdnex.ui.add_metadata_from_bdgest')
    @patch('bdnex.ui.Path')
    def test_file_processing_error_logs_exception(self, mock_path, mock_add_meta, mock_args):
        """Errors during file processing should log exception details (not swallowed silently)."""
        vargs = MagicMock()
        vargs.init = False
        vargs.input_dir = '/fake/dir'
        vargs.input_file = None
        mock_args.return_value = vargs

        fake_cbz = MagicMock()
        fake_cbz.absolute.return_value.as_posix.return_value = '/fake/dir/book.cbz'
        mock_path.return_value.rglob.side_effect = [
            [fake_cbz],  # *.cbz
            [],          # *.cbr
        ]

        error = RuntimeError("test error")
        mock_add_meta.side_effect = error

        with patch('bdnex.ui.logging') as mock_logging:
            mock_logger = MagicMock()
            mock_logging.getLogger.return_value = mock_logger

            bdnex.ui.main()

        mock_logger.exception.assert_called_once()
        call_args = mock_logger.exception.call_args[0][0]
        self.assertIn('book.cbz', call_args)
        self.assertIn('test error', call_args)
