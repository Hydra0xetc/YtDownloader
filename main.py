#!/usr/bin/env python3

import os
from log import print_error, print_red, print_yellow, show_logo
from download import download_video, download_audio
import re
import sys
import shutil
from config import load_config, ensure_download_path_exists

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def is_valid_youtube_url(url):
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

def main():
    yt_dlp = shutil.which("yt-dlp")
    if yt_dlp:
        pass
    else:
        print_error("yt-dlp not found, install it firts with: pip install yt-dlp")
        sys.exit(127)
    
    config = load_config()
    if not ensure_download_path_exists(config):
        print_error("Download path does not exist or could not be created. Exiting.")
        sys.exit(1)

    clear_screen()
    show_logo()
    print("Version: 1.1.0") # version
    while True:
        print("╭" + "─" * 30 + "╮")
        print("│ 1. Video                     │")
        print("│ 2. Audio                     │")
        print("│ 3. Exit                      │")
        print("╰" + "─" * 30 + "╯")
        try:
            user_input = int(input("Select download method: "))

            if user_input == 1:
                clear_screen()
                show_logo()
                while True:
                    print("╭" + "─" * 34 + "╮")
                    print("│ Enter video url or 0 to cancel   │")
                    print("╰" + "─" * 34 + "╯")
                    input_video_url = str(input("Enter The Url: ")).strip()
                    if is_valid_youtube_url(input_video_url):
                        download_video(input_video_url, config['video'])
                    elif input_video_url == "0":
                        clear_screen()
                        show_logo()
                        break
                    else:
                        print_error(f"'{input_video_url}' Is not a valid youtube url")

            elif user_input == 2:
                clear_screen()
                show_logo()
                while True:
                    print("╭" + "─" * 34 + "╮")
                    print("│ Enter audio url or 0 to cancel   │")
                    print("╰" + "─" * 34 + "╯")
                    input_audio_url = str(input("Enter The Url: ")).strip()
                    if is_valid_youtube_url(input_audio_url):
                        download_audio(input_audio_url, config['audio'])
                    elif input_audio_url == "0":
                        clear_screen()
                        show_logo()
                        break
                    else:
                        print_error(f"'{input_audio_url}' Is not a valid youtube url")
                    
            elif user_input == 3:
                print_red("Exiting...")
                sys.exit(0)
            else:
                print_error("Invalid option")

        except ValueError:
            print_error("Invalid Input")
        except KeyboardInterrupt:
            print_yellow("Exiting...")
            sys.exit(0)

if __name__ == "__main__":
    main()
