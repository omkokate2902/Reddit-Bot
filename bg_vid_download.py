import os
import yt_dlp

def download_youtube_video():
    print("Entering download_youtube_video function...")
    
    video_url = "https://www.youtube.com/watch?v=pQx_2LmNF8M"  # Test with a known video
    download_dir = "assets/bg_vid"
    desired_filename = "background_video.mp4"

    print(f"Checking if download directory exists: {download_dir}")
    if not os.path.exists(download_dir):
        print(f"Creating directory: {download_dir}")
        os.makedirs(download_dir)
    else:
        print(f"Directory already exists: {download_dir}")

    ydl_opts = {
        'format': 'bestvideo[height<=480][ext=mp4]/best[height<=480][ext=mp4]',
        'outtmpl': os.path.join(download_dir, desired_filename),
        'noplaylist': True,
        'verbose': True,
    }

    video_file_path = os.path.join(download_dir, desired_filename)

    if os.path.exists(video_file_path):
        print(f"Video '{desired_filename}' already exists in the download directory.")
    else:
        try:
            print(f"Preparing to download video from '{video_url}'...")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
                if os.path.exists(video_file_path):
                    print(f"'{desired_filename}' has been downloaded to {download_dir}")
                else:
                    print(f"Failed to download '{desired_filename}'. File not found.")
        except Exception as e:
            print(f"An error occurred during the download: {e}")

if __name__ == "__main__":
    try:
        print("Script is starting...")
        download_youtube_video()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")