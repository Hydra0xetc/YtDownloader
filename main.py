#!/usr/bin/env python3

from log import print_error
from download import download_video, download_audio
import re
import sys
import shutil  

def is_valid_youtube_url(url: str) -> bool:
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
    
    while True:
        print("1. Video")
        print("2. Audio")
        print("3. Exit")
        try:
            user_input = int(input("Select download method: "))

            if user_input == 1:
                while True:
                    input_video_url = str(input("Enter video url (or 0 to cancel): "))
                    if is_valid_youtube_url(input_video_url):
                        download_video(input_video_url)
                    elif input_video_url == "0":
                        break
                    else:
                        print_error("Invalid youtube url")

            elif user_input == 2:
                while True:
                    input_audio_url = str(input("Enter audio url (or 0 to cancel): ")) 
                    if is_valid_youtube_url(input_audio_url):
                        download_audio(input_audio_url)
                    elif input_audio_url == "0":
                        break
                    else:
                        print_error("Invalid youtube url")
                    
            elif user_input == 3:
                print("Exiting...")
                sys.exit(0)
            else:
                print_error("Invalid option")

        except ValueError:
            print_error("Invalid Input")
        except KeyboardInterrupt:
            print("Exiting...")
            sys.exit(0)

if __name__ == "__main__":
    main()
