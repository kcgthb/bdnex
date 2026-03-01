import logging
import unittest

from bdnex.lib.colargulog import (
    ColorCodes,
    ColorizedArgsFormatter,
    BraceFormatStyleFormatter
)


class TestColorCodes(unittest.TestCase):
    def test_color_codes_exist(self):
        """Test that color codes are defined"""
        self.assertIsNotNone(ColorCodes.grey)
        self.assertIsNotNone(ColorCodes.green)
        self.assertIsNotNone(ColorCodes.yellow)
        self.assertIsNotNone(ColorCodes.red)
        self.assertIsNotNone(ColorCodes.bold_red)
        self.assertIsNotNone(ColorCodes.blue)
        self.assertIsNotNone(ColorCodes.light_blue)
        self.assertIsNotNone(ColorCodes.purple)
        self.assertIsNotNone(ColorCodes.reset)


class TestBraceFormatStyleFormatter(unittest.TestCase):
    def setUp(self):
        self.formatter = BraceFormatStyleFormatter("%(levelname)s - %(message)s")

    def test_is_brace_format_style_with_args(self):
        """Test detection of brace format style with arguments"""
        record = logging.LogRecord(
            name="test", level=logging.INFO, pathname="", lineno=0,
            msg="Test message with {} and {}", args=("arg1", "arg2"),
            exc_info=None
        )
        self.assertTrue(BraceFormatStyleFormatter.is_brace_format_style(record))

    def test_is_brace_format_style_no_args(self):
        """Test detection fails when no args"""
        record = logging.LogRecord(
            name="test", level=logging.INFO, pathname="", lineno=0,
            msg="Test message", args=(),
            exc_info=None
        )
        self.assertFalse(BraceFormatStyleFormatter.is_brace_format_style(record))

    def test_is_brace_format_style_with_percent(self):
        """Test detection fails with percent style format"""
        record = logging.LogRecord(
            name="test", level=logging.INFO, pathname="", lineno=0,
            msg="Test message with %s", args=("arg1",),
            exc_info=None
        )
        self.assertFalse(BraceFormatStyleFormatter.is_brace_format_style(record))

    def test_is_brace_format_style_mismatched_braces(self):
        """Test detection fails with mismatched braces"""
        record = logging.LogRecord(
            name="test", level=logging.INFO, pathname="", lineno=0,
            msg="Test message with { and {}", args=("arg1", "arg2"),
            exc_info=None
        )
        self.assertFalse(BraceFormatStyleFormatter.is_brace_format_style(record))

    def test_is_brace_format_style_wrong_arg_count(self):
        """Test detection fails when arg count doesn't match placeholders"""
        record = logging.LogRecord(
            name="test", level=logging.INFO, pathname="", lineno=0,
            msg="Test message with {}", args=("arg1", "arg2"),
            exc_info=None
        )
        self.assertFalse(BraceFormatStyleFormatter.is_brace_format_style(record))

    def test_rewrite_record(self):
        """Test that record is rewritten correctly"""
        record = logging.LogRecord(
            name="test", level=logging.INFO, pathname="", lineno=0,
            msg="Test {} with {}", args=("message", "args"),
            exc_info=None
        )
        BraceFormatStyleFormatter.rewrite_record(record)
        self.assertEqual("Test message with args", record.msg)
        self.assertEqual([], record.args)

    def test_format(self):
        """Test that formatter formats correctly"""
        record = logging.LogRecord(
            name="test", level=logging.INFO, pathname="", lineno=0,
            msg="Test {} message", args=("formatted",),
            exc_info=None
        )
        formatted = self.formatter.format(record)
        self.assertIn("Test formatted message", formatted)
        # Check that original record is restored
        self.assertEqual("Test {} message", record.msg)
        self.assertEqual(("formatted",), record.args)


class TestColorizedArgsFormatter(unittest.TestCase):
    def setUp(self):
        self.formatter = ColorizedArgsFormatter("%(levelname)s - %(message)s")

    def test_init(self):
        """Test ColorizedArgsFormatter initialization"""
        self.assertIsNotNone(self.formatter.level_to_formatter)
        self.assertEqual(5, len(self.formatter.level_to_formatter))
        self.assertIn(logging.DEBUG, self.formatter.level_to_formatter)
        self.assertIn(logging.INFO, self.formatter.level_to_formatter)
        self.assertIn(logging.WARNING, self.formatter.level_to_formatter)
        self.assertIn(logging.ERROR, self.formatter.level_to_formatter)
        self.assertIn(logging.CRITICAL, self.formatter.level_to_formatter)

    def test_format_with_color(self):
        """Test that formatter adds colors correctly"""
        record = logging.LogRecord(
            name="test", level=logging.INFO, pathname="", lineno=0,
            msg="Test {} message", args=("colored",),
            exc_info=None
        )
        formatted = self.formatter.format(record)
        self.assertIn("Test", formatted)
        self.assertIn("message", formatted)
        # Check that original record is restored
        self.assertEqual("Test {} message", record.msg)
        self.assertEqual(("colored",), record.args)

    def test_format_different_levels(self):
        """Test formatting at different log levels"""
        for level in [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]:
            record = logging.LogRecord(
                name="test", level=level, pathname="", lineno=0,
                msg="Test message", args=(),
                exc_info=None
            )
            formatted = self.formatter.format(record)
            self.assertIn("Test message", formatted)


if __name__ == '__main__':
    unittest.main()
