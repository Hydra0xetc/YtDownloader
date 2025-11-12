import json
import os
from log import print_error, print_warning

CONFIG_FILE = "config.json"

DEFAULT_CONFIG = {
    "video": {
        "download_path": "/sdcard/Download/YouTubeDownload/Video/",
        "filename_template": "%(title)s - %(channel)s.%(ext)s",
        "embed_thumbnail": True,
        "embed_metadata": True
    },
    "audio": {
        "download_path": "/sdcard/Download/YouTubeDownload/Audio/",
        "filename_template": "%(title)s - %(channel)s.%(ext)s",
        "embed_thumbnail": True,
        "embed_metadata": True
    }
}

def load_config():
    config = DEFAULT_CONFIG.copy()
    
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                user_config = json.load(f)
                # Deep merge for nested structure
                if 'video' in user_config:
                    config['video'].update(user_config['video'])
                if 'audio' in user_config:
                    config['audio'].update(user_config['audio'])
        except json.JSONDecodeError:
            print_error(f"Error reading {CONFIG_FILE}. Using default configuration.")
            save_config(DEFAULT_CONFIG)
        except Exception as e:
            print_error(f"An unexpected error occurred while loading config: {e}. Using default configuration.")
            save_config(DEFAULT_CONFIG)
    else:
        print_warning(f"{CONFIG_FILE} not found. Creating with default values.")
        save_config(config)
        
    return config

def save_config(config_data):
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config_data, f, indent=2)
    except Exception as e:
        print_error(f"Error saving {CONFIG_FILE}: {e}")

# Ensure the download paths from config exist
def ensure_download_path_exists(config):
    paths_to_check = [
        config.get("video", {}).get("download_path"),
        config.get("audio", {}).get("download_path")
    ]
    
    all_paths_ok = True
    for path in paths_to_check:
        if path:
            try:
                os.makedirs(path, exist_ok=True)
            except OSError as e:
                print_error(f"Failed to create download directory {path}: {e}")
                all_paths_ok = False
    return all_paths_ok
