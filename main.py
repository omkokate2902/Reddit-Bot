
import reddit  # Import the reddit module or relevant code
import screenshot  # Import the screenshot module or relevant code
import text2speech  # Import the text2speech module or relevant code
import bg_vid_download  # Import the bg_vid_download module or relevant code
import short_clip  # Import the short_clip module or relevant code
import video_gen  # Import the video_gen module or relevant code
import html_screenshot  # Import the html_screenshot module or relevant code

user_choice = input("Options:\n1. Hottest post\n2. Trending post by time filter\n3. Post by URL\n")

if user_choice == '1':
    subreddit_name = input("Enter subreddit name: ")
    exclude_nsfw = input("Exclude NSFW content? (yes or no): ")
    time_filter=None
    post_url=None
elif user_choice == '2':
    subreddit_name = input("Enter name: ")
    exclude_nsfw = input("Is it NSFW? (yes or no): ")
    time_filter = input("Enter time filter (e.g., 'day', 'week', 'month', 'year', 'all'): ")
    post_url=None
elif user_choice == '3':
    post_url = input("Enter post URL: ")
    subreddit_name = None
    exclude_nsfw = None
    time_filter = None

# Call your functions from the imported modules here
post_info = reddit.main(user_choice, subreddit_name, exclude_nsfw, time_filter, post_url)

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
    title_comments = [post_and_comments['post_info']['title']] + [comment['comment_text'] for comment in post_and_comments['post_info']['comments']]

else:
    print("No suitable post found in the specified subreddit.")

# Call your functions from other modules as needed

# screenshot.capture_screenshots(post_id, post_url, comment_urls)

html_screenshot.update_html_with_authors_and_comments(post_id, comment_urls, title_comments)
text2speech.convert_text_to_speech(title_comments)
bg_vid_download.download_youtube_video()
short_clip.create_random_short_video()
video_gen.create_final_video()

if __name__ == "__main__":
    user_choice = "your_user_choice"
    subreddit_name = "your_subreddit_name"
    exclude_nsfw = "your_exclude_nsfw"
    time_filter = "your_time_filter"
    post_url = "your_post_url"

    # process_data(user_choice, subreddit_name, exclude_nsfw, time_filter, post_url)
