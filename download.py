import subprocess
from log import print_error, print_success
import os
import json

# NOTE: I think it would be better if a config like this was 
# created in config.json, but it's too simple if it's just a
# config like this, for now I'll leave it like this.
BASE_DOWNLOAD_DIR = "/sdcard/Download/YouTubeDownload/"

def ensure_directory_exists(path: str) -> bool:
    try:
        os.makedirs(path, exist_ok=True)
        return True
    except OSError as e:
        print_error(f"Failed to create directory {path}: {e}")
        return False

def get_info(url):
    command = [
        "yt-dlp",
        url,
        "--dump-json"
    ]

    info = subprocess.run(command, capture_output=True, text=True)
    if info.returncode == 0:
        try:
            return json.loads(info.stdout)
        except json.JSONDecodeError as e:
            print(f"Error When Parsing Json: {e}")
            return None
    else:
        print(info.stderr)
        return None 
    
def download_video(url):
    video_ext = ["webm", "mp4", "mkv", "mov"]
    info = get_info(url)
    
    if not info:
        print_error("Failed to get video information")
        return
    
    # Collect all available formats
    available_formats = []
    format_by_resolution = {}  # Group formats by resolution

    if "formats" in info:
        for format in info['formats']:
            ext = format.get('ext', '')
            has_video = format.get('vcodec') != 'none' and format.get('vcodec') is not None
            format_id = format.get('format_id', '')
            
            if ext and ext in video_ext and has_video:
                resolution = format.get('resolution', 'unknown')
                height = format.get('height', 0)
                filesize = format.get('filesize') or format.get('filesize_approx', 0)
                vcodec = format.get('vcodec', '')
                protocol = format.get('protocol', '')
                
                format_info = {
                    'resolution': resolution,
                    'height': height,
                    'filesize': filesize,
                    'format_id': format_id,
                    'ext': ext,
                    'vcodec': vcodec,
                    'protocol': protocol
                }
                
                # Group by resolution + codec + ext
                key = f"{height}p_{ext}_{vcodec[:10]}"
                
                if key not in format_by_resolution:
                    format_by_resolution[key] = []
                
                format_by_resolution[key].append(format_info)

    # Select one format per resolution group (prefer https/http over m3u8)
    for key, formats in format_by_resolution.items():
        formats.sort(key=lambda x: (
            0 if 'https' in x['protocol'] or 'http' in x['protocol'] else 1
        ))
        available_formats.append(formats[0])

    if not available_formats:
        print_error("No suitable video formats available")
        return

    # Sort by height (resolution)
    available_formats.sort(key=lambda x: x['height'], reverse=True)

    # Display formats
    print("\nAvailable formats:")
    print("=" * 60)
    
    for idx, fmt in enumerate(available_formats, 1):
        size_str = format_filesize(fmt['filesize']) if fmt['filesize'] > 0 else 'unknown'
        print(f"{idx}. {fmt['resolution']} [{fmt['ext'].upper()}] - {size_str} - {fmt['vcodec']}")
    
    print("=" * 60)

    # Get user choice
    while True:
        try:
            choice = int(input("Select format number (or 0 to cancel): "))
            
            if choice == 0:
                print("Download cancelled")
                break

            if choice < 0 or choice > len(available_formats):
                print_error("Invalid choice range")
                continue
                
            selected_format = available_formats[choice - 1]
            format_id = selected_format['format_id']
            
            # Ensure download directory exists
            if not ensure_directory_exists(BASE_DOWNLOAD_DIR):
                return
     
            # Download the video
            print(f"Selected: {selected_format['resolution']} - {selected_format['ext']}")
            
            download_command = [
                "yt-dlp",
                "-c",
                url,
                "-f", format_id,
                "-o", f"{BASE_DOWNLOAD_DIR}%(title)s.%(ext)s"
            ]
            
            result = subprocess.run(download_command)
            
            if result.returncode == 0:
                print_success(f"Downloaded Video to {BASE_DOWNLOAD_DIR}")
            else:
                print_error("Download failed")
                
        except ValueError:
            print_error("Invalid input. Please enter a number")
            continue
        except KeyboardInterrupt:
            print("Download cancelled by user")
            break

def download_audio():
    print("Not Implemented yet") 

def format_filesize(size_bytes):
    if not size_bytes or size_bytes == 0:
        return "unknown"
    return f"{size_bytes / (1024*1024):.1f} MB"
