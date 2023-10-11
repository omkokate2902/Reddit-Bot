import reddit, screenshot, text2speech

if __name__ == "__main__":
    post_id,post_url,comment_urls,post_and_comments=reddit.get_top_hot_posts(limit=1)

    screenshot.capture_screenshots(post_id,post_url, comment_urls)

    text2speech.convert_text_to_speech(post_and_comments)


