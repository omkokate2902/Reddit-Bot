import toml
import praw
import re
from jinja2 import Environment, FileSystemLoader
from playwright.sync_api import sync_playwright, ViewportSize
from PIL import Image

def read_config(filename):
    try:
        with open(filename, "r") as file:
            config = toml.load(file)
        return config
    except Exception as e:
        print("Error reading the config file:", e)
        return None

def login_to_reddit(config):
    """Log in to Reddit using PRAW."""
    return praw.Reddit(
        client_id=config['reddit']['client_id'],
        client_secret=config['reddit']['client_secret'],
        user_agent=config['reddit']['user_agent'],
        username=config['reddit']['username'],
        password=config['reddit']['password']
    )

def generate_screenshot(post_id, comment_urls):
    # Read configuration and log in to Reddit
    config = read_config("config.toml")
    if not config:
        print("Failed to read configuration.")
        return None

    reddit = login_to_reddit(config)

    # Get the submission (post) object using the post ID
    submission = reddit.submission(id=post_id)
    
    # Extract the post author's name
    post_author = submission.author.name if submission.author else '[Deleted]'
    
    # Render the HTML file with the author's name and post title
    html_file_path = render_html('title.html', author=post_author, title=submission.title)

    # Take a screenshot of the rendered HTML using Playwright
    capture_screenshots(html_file_path, 'assets/screenshots/post_screenshot.png', comment_urls, post_id)

    # Iterate through the comment URLs
    for i, comment_url in enumerate(comment_urls):
        # Extract the comment ID from the URL
        comment_id = comment_url.split('/')[-2]
        
        # Get the comment object using the comment ID
        comment = reddit.comment(id=comment_id)
        
        # Extract the comment author's name and comment text
        comment_author = comment.author.name if comment.author else '[Deleted]'
        comment_text = comment.body

        # Render the HTML file with the comment author's name and text
        html_file_path = render_html('comment.html', author=comment_author, text=comment_text)

        # Take a screenshot of the rendered HTML using Playwright
        screenshot_filename = f'assets/screenshots/comment_{i+1}_screenshot.png'
        capture_screenshots(html_file_path, screenshot_filename, [], post_id)

def render_html(template_name, **context):
    # Set up the Jinja2 environment
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template(template_name)

    # Render the template with the context
    rendered_html = template.render(**context)

    # Write the rendered HTML to the file
    html_file_path = f'templates/{template_name}'
    with open(html_file_path, 'w') as f:
        f.write(rendered_html)

    print(f"HTML file '{template_name}' has been updated with the context: {context}")
    return html_file_path

def capture_screenshots(html_file_path, output_image_path, comment_urls, post_id):
    prefix = ""

    with sync_playwright() as p:
        # Launch a headless Chromium browser
        browser = p.chromium.launch(headless=False)

        # Create a new browser context with a specific viewport size
        context = browser.new_context(viewport=ViewportSize(width=1920, height=1080))

        # Create a new page in the context
        page = context.new_page()

        try:
            # Navigate to the local HTML file
            page.goto(f'{prefix}{html_file_path}')

            # Capture a screenshot of the HTML content
            page.screenshot(path=output_image_path)

            # Open the captured screenshot with PIL for any post-processing
            image = Image.open(output_image_path)

            # Resize the image if needed
            new_width = 600
            w_percent = (new_width / float(image.size[0]))
            new_height = int((float(image.size[1]) * float(w_percent)))
            resized_image = image.resize((new_width, new_height), Image.BILINEAR)

            # Save the resized image
            resized_image.save(output_image_path)
            print(f"Captured and resized screenshot saved at {output_image_path}")

            # Capture screenshots of comments if provided
            for index, comment_url in enumerate(comment_urls, start=1):
                page.goto(f'{prefix}{comment_url}')
                page.wait_for_timeout(5000)  # Wait for 5 seconds

                comment_screenshot_path = f'{output_image_path}_comment_{index}.png'
                page.screenshot(path=comment_screenshot_path)
                print(f"Captured comment screenshot saved at {comment_screenshot_path}")

        finally:
            # Close the browser to release resources
            browser.close()

# Example usage
post_id = '1emvvvw'  # Replace with your post ID
comment_urls = [
    'https://www.reddit.com/r/AskReddit/comments/1emvvvw/who_is_an_conventionally_unattractive_person_that/lh1zqza/'
]

if __name__ == "__main__":
    generate_screenshot(post_id, comment_urls)
