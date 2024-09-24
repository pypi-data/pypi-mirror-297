"""
caption2text

A lightweight Python module to convert VTT and SRT caption files into plain text transcripts.
"""

from .converter import vtt_to_transcript, srt_to_transcript

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("caption2text")
except PackageNotFoundError:
    __version__ = "unknown"

__all__ = ["vtt_to_transcript", "srt_to_transcript"]
