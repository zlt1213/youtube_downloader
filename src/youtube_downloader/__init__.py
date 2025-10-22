"""YouTube downloader package."""

from .core import download_video
from .cli import main, parse_args

__all__ = ["download_video", "main", "parse_args"]
