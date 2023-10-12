from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip, AudioFileClip
import os

def create_final_video():

    # Input video file path (90-second video)
    video_path = 'assets/bg_vid/short_video.mp4'

    # Directory containing the images to overlay
    image_dir = 'assets/screenshots/'

    # Directory containing the audio files
    audio_dir = 'assets/voices/'

    # Output video file path
    output_path = 'output/final_video.mp4'

    # Load the video clip (90-second video)
    video_clip = VideoFileClip(video_path)

    # Initialize a list to store the composite video clips
    composite_clips = []

    # Create composite clips with each element overlaid one by one
    current_time = 0  # Keeps track of the current time in the video
    total_duration = 0  # Keeps track of the total duration of the final video

    # Add the background video to the composition
    composite_clips.append(video_clip)

    # Overlay screenshots and their respective audio
    for screenshot_number in range(1, 12):
        # Generate the filenames for the screenshot and audio
        image_file = f'screenshot_{screenshot_number}.png'
        audio_file = f'audio_{screenshot_number}.mp3'

        image_path = os.path.join(image_dir, image_file)
        audio_path = os.path.join(audio_dir, audio_file)

        # Check if the audio file exists
        if not os.path.exists(audio_path):
            break

        # Load the screenshot image
        image_clip = ImageClip(image_path)

        # Load the audio clip
        audio_clip = AudioFileClip(audio_path)

        # Calculate the remaining time available in the 90-second video
        remaining_time = 90 - total_duration

        # Check if the audio duration exceeds the remaining time
        if audio_clip.duration > remaining_time:
            # Trim the audio to fit within the remaining time
            audio_clip = audio_clip.subclip(0, remaining_time)

        # Set the image duration to match the audio duration
        image_duration = audio_clip.duration
        image_clip = image_clip.set_duration(image_duration)

        # Create a composite clip with the image and audio
        composite_clip = CompositeVideoClip([image_clip.set_position('center')], size=video_clip.size)
        composite_clip = composite_clip.set_audio(audio_clip)
        composite_clips.append(composite_clip.set_start(current_time))
        current_time += image_duration
        total_duration += image_duration

        # Check if the total duration exceeds 90 seconds
        if total_duration >= 90:
            break

    # Concatenate all the composite clips
    final_clip = CompositeVideoClip(composite_clips, size=video_clip.size)

    # Trim the final clip to 90 seconds if it exceeds
    if final_clip.duration > 90:
        final_clip = final_clip.subclip(0, 90)

    # Write the final output video
    final_clip.write_videofile(output_path, codec='libx264', audio_codec='aac', fps=video_clip.fps)
