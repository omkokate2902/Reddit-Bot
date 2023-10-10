import reddit, screenshot

if __name__ == "__main__":
    post_id,post_url,comment_urls=reddit.get_top_hot_posts(limit=1)
    # print(post_url,comment_urls)

    screenshot.capture_screenshots(post_id,post_url, comment_urls)

