import subprocess
import wcwidth
from log import print_error, print_red, print_success
import os
import json
from loading import start_loading, stop_loading

# Constants
BASE_DOWNLOAD_DIR = "/sdcard/Download/YouTubeDownload/"
VIDEO_EXTENSIONS = ["webm", "mp4", "mkv", "mov"]
AUDIO_EXTENSIONS = ["m4a", "mp3", "opus", "webm", "aac"]
MAX_BOX_WIDTH = 80

def ensure_directory_exists(path: str) -> bool:
    try:
        os.makedirs(path, exist_ok=True)
        return True
    except OSError as e:
        print_error(f"Failed to create directory {path}: {e}")
        return False

def run_yt_dlp_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout, None
    except subprocess.CalledProcessError as e:
        return None, print_error(f"yt-dlp: {e}")
    except Exception as e:
        return None, print_error(e)

def get_info(url):
    command = ["yt-dlp", url, "--dump-json"]
    
    stdout, error = run_yt_dlp_command(command)
    if error:
        print_error(error)
        return None

    if stdout is None:
        print_error("No output received from yt-dlp")
        return None

    try:
        return json.loads(stdout)
    except json.JSONDecodeError as e:
        print_error(e)
        return None

def display_width(text):
    return sum(wcwidth.wcwidth(char) for char in str(text))

def truncate_text(text, max_display_width):
    text = str(text)
    current_width = 0
    result_chars = []
    
    for char in text:
        char_width = wcwidth.wcwidth(char)
        if current_width + char_width > max_display_width - 3:
            result_chars.append("...")
            break
        result_chars.append(char)
        current_width += char_width
    
    return ''.join(result_chars)

def display_info_box(info_data, title="INFORMATION"):
    if not info_data:
        print_error("No information to display")
        return
    
    # Calculate dimensions
    max_label_width = max(display_width(label) for label, _ in info_data)
    box_width = min(MAX_BOX_WIDTH, max(60, max_label_width + 60))
    
    # Print box
    print("┌" + "─" * box_width + "┐")
    print("│" + title.center(box_width) + "│")
    print("├" + "─" * box_width + "┤")
    
    for label, value in info_data:
        available_width = box_width - max_label_width - 5
        display_value = truncate_text(value, available_width)
        
        label_str = str(label)
        value_str = str(display_value)
        
        label_padding = max_label_width - display_width(label)
        line = f"│ {label_str}{' ' * label_padding} : {value_str}"
        
        current_line_width = display_width(line) - 1
        right_padding = box_width - current_line_width
        print(line + ' ' * right_padding + "│")
    
    print("└" + "─" * box_width + "┘")

def get_video_info_data(info_dict):
    if not isinstance(info_dict, dict) or not info_dict:
        return None
    
    title = info_dict.get('title', 'Unknown')
    if title != 'Unknown' and '#' in title:
        title = title.split('#')[0].strip()
    
    return [
        ("Version", info_dict.get('_version', {}).get('version', 'Unknown')),
        ("Channel", info_dict.get('channel', 'Unknown')),
        ("Title", title),
        ("Duration", info_dict.get('duration_string', 'Unknown')),
        ("Uploader", info_dict.get('uploader', 'Unknown')),
        ("URL", info_dict.get('webpage_url', 'Unknown'))
    ]

def format_filesize(size_bytes):
    if not size_bytes or size_bytes == 0:
        return "unknown"
    return f"{size_bytes / (1024*1024):.1f} MB"

def get_best_formats(formats, extensions, is_audio=False):
    available_formats = []
    format_groups = {}
    
    for fmt in formats:
        ext = fmt.get('ext', '')
        has_content = (fmt.get('acodec') != 'none' if is_audio 
                      else fmt.get('vcodec') != 'none')
        
        if not ext or ext not in extensions or not has_content:
            continue
        

        abr = fmt.get('abr', 0)
        height = fmt.get('height', 0)

        # Create grouping key
        if is_audio:
            key = f"{int(abr)}kbps_{ext}_{fmt.get('acodec', '')[:10]}"
        else:
            key = f"{height}p_{ext}_{fmt.get('vcodec', '')[:10]}"
        
        if key not in format_groups:
            format_groups[key] = []
        
        format_info = {
            'format_id': fmt.get('format_id', ''),
            'ext': ext,
            'filesize': fmt.get('filesize') or fmt.get('filesize_approx', 0),
            'protocol': fmt.get('protocol', '')
        }
        
        # Add audio/video specific fields
        if is_audio:
            format_info.update({
                'abr': abr,
                'asr': fmt.get('asr', 0),
                'acodec': fmt.get('acodec', '')
            })
        else:
            format_info.update({
                'resolution': fmt.get('resolution', 'unknown'),
                'height': height,
                'vcodec': fmt.get('vcodec', '')
            })
        
        format_groups[key].append(format_info)
    
    # Select best format from each group (prefer http/https)
    for formats_list in format_groups.values():
        formats_list.sort(key=lambda x: (
            0 if 'https' in x['protocol'] or 'http' in x['protocol'] else 1
        ))
            
        available_formats.append(formats_list[0])
    
    # Sort by quality (bitrate for audio, height for video)
    sort_key = 'abr' if is_audio else 'height'
    available_formats.sort(key=lambda x: x[sort_key], reverse=True)
    
    return available_formats

def display_formats(formats, is_audio=False):
    if not formats:
        print_error("No suitable formats available")
        return
    
    print("Available formats:" if not is_audio else "Available audio formats:")
    print("—" * 60)
    
    for idx, fmt in enumerate(formats, 1):
        size_str = format_filesize(fmt['filesize'])
        
        if is_audio:
            bitrate = f"{int(fmt['abr'])}kbps" if fmt['abr'] > 0 else 'unknown'
            sample_rate = f"{fmt['asr']}Hz" if fmt['asr'] > 0 else ''
            print(f"{idx}. {bitrate} {sample_rate} [{fmt['ext'].upper()}] - {size_str} - {fmt['acodec']}")
        else:
            print(f"{idx}. {fmt['resolution']} [{fmt['ext'].upper()}] - {size_str} - {fmt['vcodec']}")
    
    print("—" * 60)

def get_user_choice(formats):
    while True:
        try:
            choice = input("Select format number (or 0 to cancel): ").strip()
            
            if not choice:
                continue
                
            choice = int(choice)
            
            if choice == 0:
                print("Download cancelled")
                return None
            
            if 1 <= choice <= len(formats):
                return choice - 1
            
            print_error(f"Please enter a number between 1 and {len(formats)}")
            
        except ValueError:
            print_error("Invalid input. Please enter a number")
        except KeyboardInterrupt:
            print_red("Operation cancelled by user")
            return None

def download_content(url, selected_format, content_type="Video"):
    # Ensure download directory exists
    if not ensure_directory_exists(BASE_DOWNLOAD_DIR):
        return False
    
    # Display selection info
    if content_type == "Audio":
        bitrate = f"{int(selected_format['abr'])}kbps" if selected_format['abr'] > 0 else 'unknown'
        print(f"Selected: {bitrate} - {selected_format['ext']}")
    else:
        print(f"Selected: {selected_format['resolution']} - {selected_format['ext']}")
    
    # Build download command
    download_command = [
        "yt-dlp",
        "-c",
        "--embed-metadata",
        "--embed-thumbnail",
        url,
        "-f", selected_format['format_id'],
        "-o", f"{BASE_DOWNLOAD_DIR}%(title)s.%(ext)s"
    ]
    
    # Execute download
    try:
        result = subprocess.run(download_command, check=True)
        if result.returncode == 0:
            print_success(f"Downloaded {content_type} to {BASE_DOWNLOAD_DIR}")
            return True
        else:
            print_error("Download failed")
            return False
    except subprocess.CalledProcessError:
        print_error("Download process failed")
        return False
    except KeyboardInterrupt:
        print_red("Download cancelled by user")
        return False

def download_video(url):
    start_loading()
    info = get_info(url)
    stop_loading()
    
    if not info:
        print_error("Failed to get video information")
        return
    
    # Get available formats
    available_formats = get_best_formats(info.get('formats', []), VIDEO_EXTENSIONS)
    
    if not available_formats:
        print_error("No suitable video formats available")
        return
    
    # Display information and formats
    info_data = get_video_info_data(info)
    if info_data:
        display_info_box(info_data)
    
    display_formats(available_formats)
    
    # Get user choice and download
    choice_idx = get_user_choice(available_formats)
    if choice_idx is not None:
        download_content(url, available_formats[choice_idx], "Video")

def download_audio(url):
    start_loading()
    info = get_info(url)
    stop_loading()
    
    if not info:
        print_error("Failed to get audio information")
        return
    
    # Get available formats
    available_formats = get_best_formats(info.get('formats', []), AUDIO_EXTENSIONS, is_audio=True)
    
    if not available_formats:
        print_error("No suitable audio formats available")
        return
    
    # Display information and formats
    info_data = get_video_info_data(info)
    if info_data:
        display_info_box(info_data)
    
    display_formats(available_formats, is_audio=True)
    
    # Get user choice and download
    choice_idx = get_user_choice(available_formats)
    if choice_idx is not None:
        download_content(url, available_formats[choice_idx], "Audio")
