import toml
import praw

def read_config(filename):
    try:
        with open(filename, "r") as file:
            config = toml.load(file)
        return config
    except Exception as e:
        print("Error reading the config file:", e)
        return None

def get_post_and_comments(subreddit_name, post_title, config, comment_limit):
    try:
        reddit = praw.Reddit(
            client_id=config['reddit']['client_id'],
            client_secret=config['reddit']['client_secret'],
            user_agent=config['reddit']['user_agent'],
            username=config['reddit']['username'],
            password=config['reddit']['password']
        )

        subreddit = reddit.subreddit(subreddit_name)
        post = subreddit.search(post_title, limit=1)
        
        for submission in post:
            if len(submission.comments) >= 5:
                print(f"Post Title: {submission.title}")
                print(f"Post URL: {submission.url}\n")

                comments = submission.comments[:10]
                for i, comment in enumerate(comments, start=1):
                    if not comment.stickied and not comment.body == '[removed]' and not comment.body == '[deleted]':
                        print(f"Comment {i}: {comment.body}")
            else:
                print("Fetching another post with minimum 5 comments...")
                get_another_post(subreddit, post_title, comment_limit)

    except praw.exceptions.PRAWException as e:
        print("PRAW Error:", e)
    except Exception as e:
        print("Error:", e)

def get_another_post(subreddit, post_title, comment_limit):
    for submission in subreddit.search(post_title, limit=None):
        if len(submission.comments) >= 5:
            print(f"Post Title: {submission.title}")
            print(f"Post URL: {submission.url}\n")

            comments = submission.comments[:comment_limit]
            for i, comment in enumerate(comments, start=1):
                if not comment.stickied and not comment.body == '[removed]' and not comment.body == '[deleted]':
                    print(f"Comment {i}: {comment.body}")
            break

if __name__ == "__main__":
    config_filename = "config.toml"
    config = read_config(config_filename)
    if config:
        subreddit_name = "askreddit"  # Replace with the subreddit you want to search
        post_title = "blockchain"  # Replace with the title you want to search
        comment_limit = 50  # Total number of comments to fetch
        get_post_and_comments(subreddit_name, post_title, config, comment_limit)
