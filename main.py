#!/usr/bin/env python3

import os
import re
import shutil
import subprocess
import tempfile
from log import print_success, print_error, print_debug
from typing import List, Optional, Tuple

# NOTE: I think it would be better if a config like this was created in config.json, but it's too simple if it's just a config like this, for now I'll leave it like this'
BASE_DOWNLOAD_DIR = "/sdcard/Download/YouTubeDownload/"

def is_command_available(cmd: str) -> bool:
    """Checks if a command is available in the system's PATH."""
    return shutil.which(cmd) is not None

def is_valid_youtube_url(url: str) -> bool:
    """Validates a YouTube URL using a regular expression."""
    if not url:
        return False
    pattern = re.compile(
        r"^(https?://)?(www\.)?"
        r"(youtube\.com/(watch\?v=|embed/|v/|shorts/"
        r"|playlist\?list=|user/|c/|channel/)|youtu\.be/)"
        r"[A-Za-z0-9_-]+"
        r"([?&][A-Za-z0-9_=-]+)*$"
    )
    return re.match(pattern, url) is not None

def ensure_directory_exists(path: str) -> bool:
    """Ensures a directory exists, creating it if necessary."""
    try:
        os.makedirs(path, exist_ok=True)
        return True
    except OSError as e:
        print_error(f"Failed to create directory {path}: {e}")
        return False

def check_directory_permissions(path: str) -> bool:
    """Checks for read, write, and execute permissions on a directory."""
    if not os.access(path, os.R_OK | os.W_OK | os.X_OK):
        print_error(f"Directory permissions denied: {path}")
        return False
    return True

def list_subdirectories(base_path: str) -> List[str]:
    """Lists subdirectories in a given path."""
    try:
        return [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
    except FileNotFoundError:
        return []

def select_video_quality() -> Tuple[str, str]:
    """Displays a menu for selecting video quality and returns the chosen filter."""
    qualities = [
        ("1", "bestvideo[height<=1080][vcodec!=av01][fps<=30]+bestaudio/best[height<=1080][vcodec!=av01]", "1080p"),
        ("2", "bestvideo[height<=720][vcodec!=av01][fps<=30]+bestaudio/best[height<=720][vcodec!=av01]", "720p"),
        ("3", "bestvideo[height<=480]+bestaudio/best[height<=480]", "480p"),
        ("4", "bestvideo[height<=360]+bestaudio/best[height<=360]", "360p"),
        ("5", "b", "Best Quality"),
    ]

    print("=" * 40)
    print("Select video quality:")
    for key, _, desc in qualities:
        print(f"{key}. {desc}")

    while True:
        choice = input(f"Enter choice (1-{len(qualities)}): ")
        for key, quality_filter, desc in qualities:
            if choice == key:
                print("=" * 40)
                print_debug(f"Selected: {desc}")
                return quality_filter, desc
        print_error("Invalid choice. Please try again.")


def download(url: str, quality: str, temp_dir: str, is_audio: bool) -> Optional[str]:
    """Downloads a video or audio using yt-dlp."""
    output_template = os.path.join(temp_dir, "%(title)s.%(ext)s")

    command = [
        "yt-dlp",
        "-c",
        # "-v", # Uncomment for verbose output
        "--merge-output-format", "mp4",
        "-o", output_template,
    ]

    # NOTE: i always use the best quality for audio 
    if is_audio:
        command.extend([
            "-f", "bestaudio",
            "--extract-audio",
            "--audio-format", "mp3",
            "--audio-quality", "0", # zero mean best quality
        ])
    else:
        command.extend([
            "--remux-video", "mp4",
            "-f", quality,
        ])

    command.append(url)

    try:
        print("Downloading... Please wait.")
        process = subprocess.run(command, check=True)
        print(process.stdout)
        
        # Find the downloaded file in the temp directory
        files = os.listdir(temp_dir)
        if not files:
            print_error("Download finished, but no file was found.")
            return None
            
        downloaded_file = os.path.join(temp_dir, files[0])
        print_success("Download complete.")
        return downloaded_file

    except subprocess.CalledProcessError as e:
        print_error("Download failed. Please check the URL and your connection.")
        print(f"yt-dlp stderr: {e.stderr}")
        return None
    except Exception as e:
        print_error(f"An unexpected error occurred during download: {e}")
        return None


def main():
    """Main function to run the YouTube downloader."""
    if not is_command_available("yt-dlp"):
        print_error("yt-dlp not found. Install with: pip install yt-dlp")
        return
    if not is_command_available("ffmpeg"):
        print_error("ffmpeg not found. Install using your package manager.")
        return

    if not ensure_directory_exists(BASE_DOWNLOAD_DIR):
        return

    while True:
        temp_dir = None
        try:
            print("=" * 40)
            print("Select download type:")
            print("1. Video")
            print("2. Audio")
            print("3. Exit")
            
            choice = input("Enter choice: ")

            if choice == "3":
                print("Exiting program.")
                break
            if choice not in ["1", "2"]:
                print_error("Invalid choice.")
                continue

            is_audio = (choice == "2")

            url = input("Enter YouTube URL: ")
            if not is_valid_youtube_url(url):
                print_error("Invalid YouTube URL.")
                continue

            temp_dir = tempfile.mkdtemp()
            quality = "bestaudio"
            if not is_audio:
                quality, _ = select_video_quality()

            temp_filepath = download(url, quality, temp_dir, is_audio)

            if temp_filepath:
                subdirs = list_subdirectories(BASE_DOWNLOAD_DIR)
                dest_dir = BASE_DOWNLOAD_DIR

                if subdirs:
                    print("Select a directory to save the file:")
                    for i, subdir in enumerate(subdirs):
                        print(f"{i + 1}. {subdir}")
                    print("0. Use default directory")
                    
                    dir_choice_str = input("Enter choice: ")
                    try:
                        dir_choice = int(dir_choice_str)
                        if 1 <= dir_choice <= len(subdirs):
                            dest_dir = os.path.join(BASE_DOWNLOAD_DIR, subdirs[dir_choice - 1])
                        elif dir_choice != 0:
                            print("Invalid choice, using default directory.")
                    except ValueError:
                        print("Invalid input, using default directory.")

                if not ensure_directory_exists(dest_dir) or not check_directory_permissions(dest_dir):
                    continue

                filename = os.path.basename(temp_filepath)
                dest_filepath = os.path.join(dest_dir, filename)

                try:
                    shutil.move(temp_filepath, dest_filepath)
                    print_success(f"File saved to: {dest_filepath}")
                except Exception as e:
                    print_error(f"Failed to move file: {e}")

        except KeyboardInterrupt:
            print("\nProcess cancelled by user.")
            break
        except Exception as e:
            print_error(f"An unexpected error occurred: {e}")
        finally:
            if temp_dir and os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)

if __name__ == "__main__":
    main()
