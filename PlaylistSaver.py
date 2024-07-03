from pytube import YouTube,Playlist
import time
import os
import logging
import sys
from datetime import datetime,timedelta

current_datetime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
logging.basicConfig(filename=f'yt_downloader_{current_datetime}.log', level=logging.INFO , format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

def display_message(message):
    logging.info(message)
    print(message)
    

def flush_dns():
    try:
        os.system("ipconfig /flushdns")
        display_message("DNS cache flushed successfully.")
    except Exception as e:
        display_message(f"Error flushing DNS cache: {e}")



def download_video(yt, output_path):
    video_title = yt.title
    video_title = "".join(x for x in video_title if x.isalnum() or x in [' ', '.', '_']).strip()
    try:
        display_message(f"\nDownloading video {video_title}...")
        video = yt.streams.get_highest_resolution()
        video.download(output_path)
        display_message("Video downloaded successfully.")
        return True
    except Exception as e:
        display_message(f"Error downloading video: {e}")
        return False



def process_yt_video(video_url, output_path):
    try:
        yt = YouTube(video_url)
        display_message(f"processing video URL {video_url}...")
        download_video(yt, output_path)
    except Exception as e:
        display_message(f"Invalid video URL: {e}")
        return False


def download_yt_playlist(playlist_url, output_path):
    display_message(f"\nProcessing playlist from URL: {playlist_url}")
    try:
        playlist = Playlist(playlist_url)
        playlist_name = playlist.title
        playlist_length = len(playlist.video_urls)
        total_seconds = sum([int(video.length) for video in playlist.videos])
        playlist_duration = str(timedelta(seconds=total_seconds))
        if playlist_length > 0:
            average_length_seconds = total_seconds / playlist_length
            average_length = str(timedelta(seconds=int(average_length_seconds)))
        else:
            average_length = "N/A"
        
        display_message(f'Playlist Name: {playlist_name}')
        display_message(f'Number of Videos: {playlist_length}')
        display_message(f'Playlist Duration: {playlist_duration}')
        display_message(f'Average Length of Video: {average_length}')

        playlist_folder = os.path.join(output_path, playlist_name)
        if not os.path.exists(playlist_folder):
            os.makedirs(playlist_folder)
            display_message(f'''Created folder "{playlist_name}" at "{playlist_folder}"''')
        else:
            display_message(f"Folder already exists at {playlist_folder}")

        unsuccessful_videos = []
        for video in playlist.videos:
            try:
                if (not download_video(video, playlist_folder)):
                    unsuccessful_videos.append(video)
            except Exception as e:
                display_message(f"Error processing video: {e}")

        if len(unsuccessful_videos) > 0:
            display_message(f"Unsuccessful downloads: {len(unsuccessful_videos)}")
            display_message(f"Retrying unsuccessful downloads...")
            for video in unsuccessful_videos:
                time.sleep(3)
                try:
                    download_video(video, playlist_folder)
                except Exception as e:
                    display_message(f"Error processing video: {e}")
    except Exception as e:
        display_message(f'Error fetching playlist details: {str(e)}')
        return False



if __name__ == "__main__":
    flush_dns()
    sys.stdout.write("\033c") # Clear the screen
    sys.stdout.flush()
    
    choice = input("Enter '1' to download a video or '2' to download a playlist: ")

    if choice == '1':
        video_url = input("Enter the video URL: ")
        output_path = input("Enter the output path: ")
        logging.info(f"Processing video URL: {video_url}")
        process_yt_video(video_url, output_path)
    elif choice == '2':
        playlist_url = input("Enter the playlist URL: ")
        output_path = input("Enter the output path: ")
        logging.info(f"Processing video URL: {playlist_url}")
        download_yt_playlist(playlist_url, output_path)
    else:
        display_message("Invalid choice. Please enter '1' or '2': ")