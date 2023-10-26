import reddit, screenshot, text2speech, bg_vid_download, short_clip, video_gen


post_info = reddit.main()

if post_info:
    post_id = post_info["id"]
    post_url = post_info["url"]
    comment_urls = [comment["comment_url"] for comment in post_info["comments"]]
    post_and_comments = {
        "post_id": post_id,
        "post_url": post_url,
        "comment_urls": comment_urls,
        "post_info": post_info
    }
    # print(post_and_comments)
else:
    print("No suitable post found in the specified subreddit.")


screenshot.capture_screenshots(post_id,post_url,comment_urls)

text2speech.convert_text_to_speech(post_and_comments)

bg_vid_download.download_youtube_video()

short_clip.create_random_short_video()

video_gen.create_final_video()
