from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import time

# Import your project-specific modules
import reddit
import html_screenshot
import text2speech
import bg_vid_download
import short_clip
import video_gen

global post_id, post_url, comment_urls, post_and_comments

app = Flask(__name__, static_folder='static')
CORS(app)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_video', methods=['POST'])
def generate_video():

    socketio.emit('task_update', {'message': 'Video generation started'})

    global post_id, post_url, comment_urls, post_and_comments

    data = request.get_json()

    user_choice = data.get('userChoice')
    subreddit_name = data.get('subredditName')
    exclude_nsfw = True  # Keeping NSFW exclusion enabled as per your requirement
    time_filter = data.get('timeFilter')
    post_url = data.get('postUrl')

    print(f"Received form data: {data}")

    # Fetch Reddit post information based on user input
    post_info = reddit.main(user_choice, subreddit_name, exclude_nsfw, time_filter, post_url)
    
    if post_info:
        post_id = post_info["id"]
        post_url = post_info["url"]
        comment_urls = [comment["comment_url"] for comment in post_info["comments"]]
        title = post_info.get("title", "")
        comments = [comment.get("comment_text", "") for comment in post_info.get("comments", [])]
        title_comments = [title] + comments
        
        # Update HTML with authors and comments
        html_screenshot.update_html_with_authors_and_comments(post_id, comment_urls, title_comments)

        # Emit updates through WebSocket
        socketio.emit('task_update', {'message': 'HTML updated with authors and comments'})

        # Process the remaining tasks
        text2speech.convert_text_to_speech(title_comments)
        socketio.emit('task_update', {'message': 'Text-to-speech conversion completed'})

        bg_vid_download.download_youtube_video()
        socketio.emit('task_update', {'message': 'Background video downloaded'})

        short_clip.create_random_short_video()
        socketio.emit('task_update', {'message': 'Short video created'})

        video_gen.create_final_video()
        socketio.emit('task_update', {'message': 'Final video generated'})

        # Return success response
        return jsonify({"message": "Video generation done."})
    else:
        return jsonify({"error": "No suitable post found in the subreddit."}), 400

@socketio.on('connect')
def handle_connect():
    print("Client connected")

@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8000, debug=True)