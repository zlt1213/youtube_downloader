"""Command-line utility to download YouTube videos as MP4 files.

This script uses the ``yt-dlp`` package to fetch and merge the best
available audio and video streams into an MP4 container.  It requires
``ffmpeg`` to be installed and accessible on the system ``PATH``.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Iterable

try:
    import yt_dlp  # type: ignore
except ImportError as exc:  # pragma: no cover - import guard
    raise SystemExit(
        "The 'yt_dlp' package is required to run this script.\n"
        "Install it with 'pip install yt-dlp' and try again."
    ) from exc


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
        default=Path.cwd(),
        type=Path,
        help="Directory where the downloaded MP4 should be saved (defaults to current directory).",
    )
    return parser.parse_args(list(argv) if argv is not None else None)


def download_video(url: str, output_dir: Path) -> Path:
    """Download ``url`` into ``output_dir`` and return the resulting file path."""

    output_dir.mkdir(parents=True, exist_ok=True)

    # ``yt-dlp`` configuration that prefers MP4 output when possible and merges
    # separate audio/video streams into a single MP4 file via ffmpeg.
    ydl_opts = {
        "outtmpl": str(output_dir / "%(title)s.%(ext)s"),
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best",
        "merge_output_format": "mp4",
        "postprocessors": [
            {
                "key": "FFmpegVideoConvertor",
                "preferedformat": "mp4",
            }
        ],
        "quiet": False,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(url, download=True)

    # ``result`` is a mapping; ``_filename`` contains the final path.
    filename = result.get("_filename")
    if not filename:
        raise RuntimeError("Failed to determine the output filename from yt-dlp.")

    return Path(filename)


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


if __name__ == "__main__":  # pragma: no cover - CLI entrypoint
    raise SystemExit(main())
