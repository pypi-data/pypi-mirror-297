"""Unit tests for the converter module."""

import unittest
import os
import sys
import difflib

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from caption2text import vtt_to_transcript, srt_to_transcript


class TestConverter(unittest.TestCase):
    """Test cases for the Converter class."""

    def setUp(self):
        self.test_data_dir = os.path.join(os.path.dirname(__file__), "test_data")
        self.vtt_file = os.path.join(self.test_data_dir, "sample.vtt")
        self.srt_file = os.path.join(self.test_data_dir, "sample.srt")
        self.txt_file = os.path.join(self.test_data_dir, "sample.txt")

    def test_vtt_to_transcript(self):
        """Test conversion of VTT file to transcript format."""
        vtt_transcript = vtt_to_transcript(self.vtt_file)

        with open(self.txt_file, "r", encoding="utf-8") as f:
            expected_transcript = f.read().strip()

        try:
            self.assertEqual(
                vtt_transcript,
                expected_transcript,
                "VTT conversion failed: The transcript does not match the expected output.",
            )
        except AssertionError:
            diff = difflib.unified_diff(
                expected_transcript.splitlines(keepends=True),
                vtt_transcript.splitlines(keepends=True),
                fromfile="expected",
                tofile="actual",
            )
            print("\n".join(diff))
            raise

    def test_srt_to_transcript(self):
        """Test conversion of SRT file to transcript format."""
        srt_transcript = srt_to_transcript(self.srt_file)

        with open(self.txt_file, "r", encoding="utf-8") as f:
            expected_transcript = f.read().strip()

        try:
            self.assertEqual(
                srt_transcript,
                expected_transcript,
                "SRT conversion failed: The transcript does not match the expected output.",
            )
        except AssertionError:
            diff = difflib.unified_diff(
                expected_transcript.splitlines(keepends=True),
                srt_transcript.splitlines(keepends=True),
                fromfile="expected",
                tofile="actual",
            )
            print("\n".join(diff))
            raise


if __name__ == "__main__":
    unittest.main()
