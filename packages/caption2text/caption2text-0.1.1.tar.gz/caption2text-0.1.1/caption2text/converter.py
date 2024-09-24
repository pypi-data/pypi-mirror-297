"""Module for converting VTT and SRT files to plain text transcripts."""

import argparse
import sys
import re
import logging
from typing import List

logging.basicConfig(level=logging.INFO)

# Precompile regular expressions for performance
VTT_HEADER_REGEX = re.compile(r"^(WEBVTT.*|\s*Kind:.*|\s*Language:.*)$", re.MULTILINE)
VTT_TIMESTAMP_REGEX = re.compile(r"\d{2}:\d{2}:\d{2}\.\d{3} --> .*")
HTML_TAG_REGEX = re.compile(r"<[^>]+>|{[^}]+}")
EMPTY_LINE_REGEX = re.compile(r"^\s*$", re.MULTILINE)
SRT_INDEX_REGEX = re.compile(r"^\d+$", re.MULTILINE)
SRT_TIMESTAMP_REGEX = re.compile(r"\d{2}:\d{2}:\d{2},\d{3} --> .*")


def _remove_empty_lines_and_tags(content: str) -> str:
    """Remove empty lines and HTML-like tags from the content."""
    content = EMPTY_LINE_REGEX.sub("", content)
    content = HTML_TAG_REGEX.sub("", content)
    return content


def _process_lines(lines: List[str]) -> str:
    """Process and join lines into a transcript."""
    return "\n".join(line.strip() for line in lines if line.strip())


def vtt_to_transcript(vtt_file_path: str) -> str:
    """
    Convert a VTT file to a plain text transcript.

    Args:
        vtt_file_path (str): Path to the VTT file.

    Returns:
        str: Plain text transcript.

    Raises:
        FileNotFoundError: If the file is not found.
        IOError: If there's an error reading the file.
        Exception: For any other unexpected errors.
    """
    logging.info("Converting VTT file '%s' to transcript.", vtt_file_path)
    try:
        with open(vtt_file_path, "r", encoding="utf-8") as file:
            content = file.read()

        content = VTT_HEADER_REGEX.sub("", content)
        content = VTT_TIMESTAMP_REGEX.sub("", content)
        content = _remove_empty_lines_and_tags(content)

        return _process_lines(content.split("\n"))
    except FileNotFoundError:
        logging.error("VTT file '%s' not found.", vtt_file_path)
        raise
    except IOError as e:
        logging.error("Error reading VTT file '%s': %s", vtt_file_path, str(e))
        raise
    except Exception as e:
        logging.error(
            "Unexpected error converting VTT file '%s': %s", vtt_file_path, str(e)
        )
        raise


def srt_to_transcript(srt_file_path: str) -> str:
    """
    Convert an SRT file to a plain text transcript.

    Args:
        srt_file_path (str): Path to the SRT file.

    Returns:
        str: Plain text transcript.

    Raises:
        FileNotFoundError: If the file is not found.
        IOError: If there's an error reading the file.
        Exception: For any other unexpected errors.
    """
    logging.info("Converting SRT file '%s' to transcript.", srt_file_path)
    try:
        with open(srt_file_path, "r", encoding="utf-8") as file:
            content = file.read()

        content = SRT_INDEX_REGEX.sub("", content)
        content = SRT_TIMESTAMP_REGEX.sub("", content)
        content = _remove_empty_lines_and_tags(content)

        return _process_lines(content.split("\n"))
    except FileNotFoundError:
        logging.error("SRT file '%s' not found.", srt_file_path)
        raise
    except IOError as e:
        logging.error("Error reading SRT file '%s': %s", srt_file_path, str(e))
        raise
    except Exception as e:
        logging.error(
            "Unexpected error converting SRT file '%s': %s", srt_file_path, str(e)
        )
        raise


def main():
    parser = argparse.ArgumentParser(
        description="Convert VTT or SRT files to plain text transcripts."
    )
    parser.add_argument("command", choices=["convert"], help="The command to execute")
    parser.add_argument("file_path", help="Path to the VTT or SRT file")
    args = parser.parse_args()

    if args.command == "convert":
        file_path = args.file_path
        if file_path.lower().endswith(".vtt"):
            try:
                transcript = vtt_to_transcript(file_path)
                print(transcript)
            except Exception as e:
                print(f"Error: {str(e)}", file=sys.stderr)
                sys.exit(1)
        elif file_path.lower().endswith(".srt"):
            try:
                transcript = srt_to_transcript(file_path)
                print(transcript)
            except Exception as e:
                print(f"Error: {str(e)}", file=sys.stderr)
                sys.exit(1)
        else:
            print(
                "Error: Unsupported file format. Please use .vtt or .srt files.",
                file=sys.stderr,
            )
            sys.exit(1)


if __name__ == "__main__":
    main()
