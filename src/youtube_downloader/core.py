"""Core functionality for downloading YouTube videos as MP4 files."""

from __future__ import annotations

from pathlib import Path

try:
    import yt_dlp  # type: ignore
except ImportError as exc:  # pragma: no cover - import guard
    raise SystemExit(
        "The 'yt_dlp' package is required to run this script.\n"
        "Install it with 'pip install yt-dlp' and try again."
    ) from exc


__all__ = ["download_video"]


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
