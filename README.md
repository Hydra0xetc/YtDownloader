# YtDownloader

A simple, command-line tool to download videos and audio from YouTube.

## Features

-   **Download Video or Audio**: Choose to download a full video or extract the audio.
-   **Quality Selection**: Lists available video resolutions (e.g., 1080p, 720p) and audio bitrates, allowing you to choose the desired quality.
-   **Detailed Information**: Displays video details like title, channel, duration, and uploader before downloading.
-   **Interactive CLI**: An easy-to-use interactive command-line interface.
-   **Organized Downloads**: Saves all files to dedicated folders based on your configuration.
-   **Customizable Settings**: Adjust download paths, filename formats, and embedding options via a `config.json` file.

## Prerequisites

-   **Python 3**: The script is written in Python and requires a Python 3 environment.
-   **yt-dlp**: A powerful command-line program to download videos from YouTube and other sites. The script checks if `yt-dlp` is in your PATH.

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/Hydra0xetc/YtDownloader.git
    ```

2.  Navigate to the project directory:
    ```bash
    cd YtDownloader/
    ```

3.  Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```
## Usage

1.  Run the main script from within the `python` directory:
    ```bash
    python main.py
    ```

2.  The script will display a menu. Choose whether you want to download a **Video** (1) or **Audio** (2).

3.  Enter the YouTube URL when prompted.

4.  The script will fetch video information and display it, along with a list of available formats (e.g., resolution for videos, bitrate for audio).

5.  Select your desired format by entering the corresponding number.

6.  The download will begin.

## Configuration

The `config.json` file allows you to customize various aspects of the downloader. If the file doesn't exist, it will be created automatically with default values.

Here's an example of the `config.json` structure:

```json
{
  "video": {
    "download_path": "/sdcard/Download/YouTubeDownload/Video/",
    "filename_template": "%(title)s - %(channel)s.%(ext)s",
    "embed_thumbnail": true,
    "embed_metadata": true
  },
  "audio": {
    "download_path": "/sdcard/Download/YouTubeDownload/Audio/",
    "filename_template": "%(title)s - %(channel)s.%(ext)s",
    "embed_thumbnail": true,
    "embed_metadata": true
  }
}
```

**Options:**
-   `download_path`: The directory where downloaded files will be saved.
-   `filename_template`: A template string for naming the output files. You can use `yt-dlp`'s output template variables (e.g., `%(title)s`, `%(channel)s`, `%(ext)s`).
-   `embed_thumbnail`: Set to `true` to embed the video thumbnail into the downloaded file (if the format supports it), or `false` to skip.
-   `embed_metadata`: Set to `true` to embed metadata into the downloaded file, or `false` to skip.

## Default Download Location

By default, files are saved to:
-   Videos: `/sdcard/Download/YouTubeDownload/Video/`
-   Audios: `/sdcard/Download/YouTubeDownload/Audio/`

These directories will be created if they do not exist.
