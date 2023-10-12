import random
from moviepy.editor import VideoFileClip

def create_random_short_video():

    input_video = "assets/bg_vid/background_video.mp4"
    # Output video file path for the random 90-second clip in 9:16 portrait aspect ratio
    output_video = "assets/bg_vid/short_video.mp4"

    # Get the duration of the input video
    video_clip = VideoFileClip(input_video)
    video_duration = video_clip.duration

    # Ensure the video is at least 90 seconds long
    if video_duration < 90:
        print("Error: The video is shorter than 90 seconds.")
    else:
        # Calculate a random start time within the valid range
        start_time = random.uniform(0, video_duration - 90)

        # Extract the random 90-second clip
        output_clip = video_clip.subclip(start_time, start_time + 90)

        # Crop the center portion to achieve a 9:16 portrait aspect ratio
        width, height = output_clip.size
        aspect_ratio = 9 / 16

        # Calculate the new width based on the aspect ratio
        new_width = int(height * aspect_ratio)

        # Calculate the cropping margins to keep the center
        left_margin = (width - new_width) // 2
        right_margin = width - left_margin

        # Apply cropping
        output_clip = output_clip.crop(x1=left_margin, x2=right_margin)

        # Resize the output clip to 720x1280 (portrait)
        output_clip = output_clip.resize((720, 1280))

        # Write the output video
        output_clip.write_videofile(output_video, codec="libx264")
