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

def is_valid_comment(comment):
    return comment.body != '[deleted]' and comment.body != '[removed]' and len(comment.body) <= 80

def print_post_info(post_info):
    print(f"ID: {post_info['id']}")
    print(f"Title: {post_info['title']}")
    print(f"URL: {post_info['url']}")
    print("Comments:")
    for i, comment_info in enumerate(post_info['comments'], start=1):
        print(f"Comment {i}: {comment_info['comment_text']}")
        print(f"Comment URL {i}: {comment_info['comment_url']}")
    print("\n")

def get_hottest_post(subreddit_name, exclude_nsfw, check_comments=True, min_comments=5, max_comments=10):
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

            subreddit = reddit.subreddit(subreddit_name)

            # Fetch the hottest post
            hot_post = subreddit.hot(limit=1).__next__()

            if not hot_post.over_18 or not exclude_nsfw:
                post_info = {
                    "id": hot_post.id,
                    "title": hot_post.title,
                    "url": hot_post.url,
                    "comments": []
                }

                if check_comments:
                    comments_count = 0
                    for comment in hot_post.comments:
                        if isinstance(comment, praw.models.Comment) and is_valid_comment(comment):
                            cleaned_comment = beautify_comment(comment.body)
                            comment_info = {
                                "comment_text": cleaned_comment,
                                "comment_url": f"{hot_post.url}{comment.id}/"
                            }
                            post_info["comments"].append(comment_info)
                            comments_count += 1

                            if comments_count >= max_comments:
                                break

                if len(post_info["comments"]) < min_comments:
                    print("The hottest post doesn't have enough suitable comments.")
                    return None

                return post_info
            else:
                print("The hottest post is NSFW and is excluded.")
                return None

        except praw.exceptions.PRAWException as e:
            print("PRAW Error:", e)
        except Exception as e:
            print("Error:", e)

def get_top_posts(subreddit_name, exclude_nsfw, time_filter='week', check_comments=True, min_comments=5, max_comments=10):
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

            subreddit = reddit.subreddit(subreddit_name)

            # Map time filter options to PRAW's time options
            time_filters = {
                'now': 'hour',
                'today': 'day',
                'week': 'week',
                'month': 'month',
                'year': 'year',
                'all time': 'all',
            }

            time_filter = time_filters.get(time_filter.lower(), 'week')

            # Fetch the top post based on the specified time filter
            top_posts = subreddit.top(time_filter=time_filter, limit=1)

            post_info = None

            for post in top_posts:
                if not post.over_18 or not exclude_nsfw:
                    post_info = {
                        "id": post.id,
                        "title": post.title,
                        "url": post.url,
                        "comments": []
                    }

                    if check_comments:
                        comments_count = 0
                        for comment in post.comments:
                            if isinstance(comment, praw.models.Comment) and is_valid_comment(comment):
                                cleaned_comment = beautify_comment(comment.body)
                                comment_info = {
                                    "comment_text": cleaned_comment,
                                    "comment_url": f"{post.url}{comment.id}/"
                                }
                                post_info["comments"].append(comment_info)
                                comments_count += 1

                            if comments_count >= max_comments:
                                break

                    if not post_info["comments"]:
                        print(f"No suitable comments found for the top post of {time_filter}.")
                        return None

                    return post_info

            print(f"No suitable posts found for the top post of {time_filter}.")
            return None

        except praw.exceptions.PRAWException as e:
            print("PRAW Error:", e)
        except Exception as e:
            print("Error:", e)

def get_post_by_url(post_url, check_comments=True, min_comments=5, max_comments=10):
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

            # Extract the post ID from the URL
            post_id = post_url.split('/')[-3]

            post = reddit.submission(id=post_id)

            if not post.over_18 or not exclude_nsfw:
                post_info = {
                    "id": post.id,
                    "title": post.title,
                    "url": post.url,
                    "comments": []
                }

                if check_comments:
                    comments_count = 0
                    for comment in post.comments:
                        if isinstance(comment, praw.models.Comment) and is_valid_comment(comment):
                            cleaned_comment = beautify_comment(comment.body)
                            comment_info = {
                                "comment_text": cleaned_comment,
                                "comment_url": f"{post.url}{comment.id}/"
                            }
                            post_info["comments"].append(comment_info)
                            comments_count += 1

                    if not post_info["comments"]:
                        print("No suitable comments found for the specified post.")
                        return None

                return post_info
            else:
                print("The specified post is NSFW and is excluded.")
                return None

        except praw.exceptions.PRAWException as e:
            print("PRAW Error:", e)
        except Exception as e:
            print("Error:", e)

def main():
    print("Options:")
    print("1. Fetch Hottest Post")
    print("2. Fetch Top Post by Time Filter")
    print("3. Fetch Post by URL")

    user_choice = input("Enter your choice (1/2/3): ")
    subreddit_name = None
    exclude_nsfw = False

    if user_choice in ("1", "2"):
        subreddit_name = input("Enter the subreddit name: ")
        exclude_nsfw_choice = input("Exclude NSFW posts? (yes/no): ")
        exclude_nsfw = exclude_nsfw_choice.lower() == "yes"

    post_info = None

    if user_choice == "1":
        post_info = get_hottest_post(subreddit_name, exclude_nsfw)
    elif user_choice == "2":
        time_filter = input("Enter the time filter (now/today/week/month/year/all time): ")
        post_info = get_top_posts(subreddit_name, exclude_nsfw, time_filter)
    elif user_choice == "3":
        post_url = input("Enter the post URL: ")
        post_info = get_post_by_url(post_url)

    if post_info:
        return post_info
    else:
        print("No suitable post found.")
        return None

if __name__ == "__main__":
    print("run through main.py")
    # main()
