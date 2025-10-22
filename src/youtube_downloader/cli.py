"""Command-line interface for the YouTube downloader."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Iterable

from .core import download_video

__all__ = ["parse_args", "main"]


DEFAULT_DOWNLOAD_DIR = Path(__file__).resolve().parents[2] / "download"


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(
        description="Download a YouTube video as an MP4 file.",
    )
    parser.add_argument(
        "url",
        help="The URL of the YouTube video to download.",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=DEFAULT_DOWNLOAD_DIR,
        type=Path,
        help="Directory where the downloaded MP4 should be saved (defaults to the project's 'download' folder).",
    )
    return parser.parse_args(list(argv) if argv is not None else None)


def main(argv: Iterable[str] | None = None) -> int:
    """Entrypoint for the command-line interface."""

    args = parse_args(argv)

    try:
        final_path = download_video(args.url, args.output)
    except Exception as exc:  # pragma: no cover - runtime failure path
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(f"Downloaded video to: {final_path}")
    return 0
