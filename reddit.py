import toml
import praw
import re

def read_config(filename):
    try:
        with open(filename, "r") as file:
            config = toml.load(file)
        return config
    except Exception as e:
        print("Error reading the config file:", e)
        return None

def beautify_comment(comment_text):
    # Remove links using regular expression
    cleaned_comment = re.sub(r'http\S+', '', comment_text)
    return cleaned_comment

def get_top_hot_posts(limit):
    config = read_config("config.toml")
    if config:
        try:
            reddit = praw.Reddit(
                client_id=config['reddit']['client_id'],
                client_secret=config['reddit']['client_secret'],
                user_agent=config['reddit']['user_agent'],
                username=config['reddit']['username'],
                password=config['reddit']['password']
            )

            subreddit_name = config['reddit']['subreddit_name']
            comment_limit = config['reddit']['comment_limit']
            exclude_nsfw = config['reddit']['exclude_nsfw']

            subreddit = reddit.subreddit(subreddit_name)
            hot_posts = subreddit.hot(limit=None)  # Fetch all hot posts

            top_hot_posts = []
            for post in hot_posts:
                if not post.over_18 and (not exclude_nsfw or (exclude_nsfw and not post.over_18)):
                    post_info = {
                        "id": post.id,
                        "title": post.title,
                        "url": post.url,
                        "comments": []
                    }

                    comments = post.comments.list()[:comment_limit]
                    for i, comment in enumerate(comments, start=1):
                        if not comment.stickied and not comment.body == '[removed]' and not comment.body == '[deleted]':
                            cleaned_comment = beautify_comment(comment.body)
                            if cleaned_comment:
                                comment_info = {
                                    "comment_text": cleaned_comment,
                                    "comment_url": f"{post.url}{comment.id}/"
                                }
                                post_info["comments"].append(comment_info)

                    top_hot_posts.append(post_info)
                    if len(top_hot_posts) >= limit:
                        break  # Stop when you have collected enough posts

            for i, post in enumerate(top_hot_posts, start=1):
                print(f"Post {i}:")
                print(f"ID: {post['id']}")
                print(f"Title: {post['title']}")
                print(f"URL: {post['url']}")
                print("Comments:")
                for j, comment_info in enumerate(post['comments'], start=1):
                    print(f"Comment {j}: {comment_info['comment_text']}")
                    print(f"Comment URL {j}: {comment_info['comment_url']}")
                print("\n")
            
            post_id = top_hot_posts[0]['id']
            post_url = top_hot_posts[0]['url']
            comment_urls = [comment['comment_url'] for comment in top_hot_posts[0]['comments']]

            post_title = top_hot_posts[0]['title']
            comments = [comment['comment_text'] for comment in top_hot_posts[0]['comments']]
            post_and_comments = [post_title] + comments
            
            return post_id,post_url,comment_urls,post_and_comments

        except praw.exceptions.PRAWException as e:
            print("PRAW Error:", e)
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    limit = 1
    posts = get_top_hot_posts(limit)
