# YouTube Downloader

This project provides a command-line interface for downloading YouTube videos as MP4 files using [yt-dlp](https://github.com/yt-dlp/yt-dlp).

## Project layout

```
.
├── README.md
├── download/
│   └── .gitkeep
├── src/
│   └── youtube_downloader/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli.py
│       └── core.py
└── youtube_downloader.py
```

The core download logic lives in `src/youtube_downloader/core.py`, while the CLI argument parsing and entrypoint are defined in `src/youtube_downloader/cli.py`.

## Usage

1. Install dependencies:
   ```bash
   pip install yt-dlp
   ```

   Ensure `ffmpeg` is available on your system `PATH`.

2. Run the downloader either via the compatibility wrapper:
   ```bash
   python youtube_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID" -o /path/to/output
   ```

   or directly via the package using the `src` layout:
   ```bash
   PYTHONPATH=src python -m youtube_downloader "https://www.youtube.com/watch?v=VIDEO_ID" -o /path/to/output
   ```

Without any flags the downloader saves MP4 files into the project's bundled `download/` directory, creating it automatically as needed. Use `-o/--output` to override the target directory. The command prints the final MP4 path when the download succeeds and exits with code `0`. Errors are printed to `stderr` and return a non-zero exit status.
