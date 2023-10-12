import os
from pytube import YouTube

# Function to download a YouTube video if it doesn't already exist
def download_youtube_video():

    video_url = "https://www.youtube.com/watch?v=n_Dv4JMiwK8&t=1345s&ab_channel=bbswitzer"
    download_dir = "assets/bg_vid"
    desired_filename = "background_video.mp4"

    yt = YouTube(video_url)
    video_stream = yt.streams.get_highest_resolution()
    video_title = yt.title

    # Check if the video file already exists in the download directory with the desired filename
    video_file_path = os.path.join(download_dir, desired_filename)

    if os.path.exists(video_file_path):
        print(f"Video '{desired_filename}' already exists in the download directory.")
    else:
        print(f"Downloading '{video_title}' as '{desired_filename}'...")
        video_stream.download(output_path=download_dir, filename=desired_filename)
        print(f"'{desired_filename}' has been downloaded to {download_dir}")
