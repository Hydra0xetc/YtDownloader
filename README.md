# YouTube Downloader

A simple, command-line tool to download videos and audio from YouTube.

## Features

-   **Download Videos and Audio**: Easily download either video (MP4) or audio-only (MP3) from a YouTube URL.
-   **Quality Selection**: Choose from a list of available video qualities (1080p, 720p, 480p, etc.) before downloading.
-   **Directory Management**: Save files to a default download directory or choose from a list of existing subdirectories.
-   **Command-line Interface**: Interactive and easy to use directly from your terminal.

## Prerequisites

Before running this script, you need to have the following installed on your system:

1.  **Python 3**: The script is written in Python and requires a Python 3 environment.
2.  **yt-dlp**: A powerful command-line program to download videos from YouTube and other sites.
    -   Installation: `pip install yt-dlp`
3.  **FFmpeg**: A complete, cross-platform solution to record, convert and stream audio and video. `yt-dlp` requires it for merging video and audio streams.
    -   Installation: Use your system's package manager (e.g., `apt install ffmpeg`, `brew install ffmpeg`).

## How to Use

1.  Run the main script:
    ```bash
    python main.py
    ```
2.  Follow the on-screen prompts to:
    -   Select the download type (Video or Audio).
    -   Enter the YouTube URL.
