from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

import reddit  # Import the reddit module or relevant code
# import screenshot  # Import the screenshot module or relevant code
import html_screenshot  # Import the html_screenshot module or relevant code
import text2speech  # Import the text2speech module or relevant code
import bg_vid_download  # Import the bg_vid_download module or relevant code
import short_clip  # Import the short_clip module or relevant code
import video_gen  # Import the video_gen module or relevant code

global post_id, post_url, comment_urls, post_and_comments


app = Flask(__name__, static_folder='static')
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_video', methods=['POST'])
def generate_video():
    global post_id, post_url, comment_urls, post_and_comments

    data = request.get_json()

    user_choice = data.get('userChoice')
    subreddit_name = data.get('subredditName')
    # exclude_nsfw = data.get('excludeNsfw')
    exclude_nsfw = True
    time_filter = data.get('timeFilter')
    post_url = data.get('postUrl')



    print("Received form data:")
    print(f"userChoice: {user_choice}")
    print(f"subredditName: {subreddit_name}")
    print(f"excludeNsfw: {exclude_nsfw}")
    print(f"timeFilter: {time_filter}")
    print(f"postUrl: {post_url} \n")

    post_info = reddit.main(user_choice, subreddit_name, exclude_nsfw, time_filter, post_url)

    # print(post_info)
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
        print(post_and_comments)
    else:
        print("No suitable post found in the specified subreddit.")

    title = post_info.get("title", "")
    comments = [comment.get("comment_text", "") for comment in post_info.get("comments", [])]

    # Combine the title and comments into a single list
    title_comments = [title] + comments

    html_screenshot.update_html_with_authors_and_comments(post_id, comment_urls, title_comments)
    # screenshot.capture_screenshots(post_id, post_url, comment_urls)
    text2speech.convert_text_to_speech(title_comments)
    bg_vid_download.download_youtube_video()
    short_clip.create_random_short_video()
    video_gen.create_final_video()

    # Process the data and generate the video as needed
    # You can call your Python functions and return the result here

    # For demonstration purposes, we'll return a message
    response_message = "Video generation done."

    return jsonify({"message": response_message})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
