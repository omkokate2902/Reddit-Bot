import reddit, screenshot, text2speech, bg_vid_download, short_clip, video_gen

if __name__ == "__main__":

    post_id,post_url,comment_urls,post_and_comments=reddit.get_top_hot_posts(limit=1)

    screenshot.capture_screenshots(post_id,post_url,comment_urls)

    text2speech.convert_text_to_speech(post_and_comments)

    bg_vid_download.download_youtube_video()

    short_clip.create_random_short_video()

    video_gen.create_final_video()