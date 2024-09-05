import toml
import praw
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import os

# Function to read the configuration from a TOML file
def read_config(filename):
    try:
        with open(filename, "r") as file:
            config = toml.load(file)
        return config
    except Exception as e:
        print("Error reading the config file:", e)
        return None

# Load the configuration from the config.toml file
config = read_config("config.toml")

if config:
    # Initialize PRAW using credentials from the config file
    reddit = praw.Reddit(
        client_id=config['reddit']['client_id'],
        client_secret=config['reddit']['client_secret'],
        user_agent=config['reddit']['user_agent'],
        username=config['reddit']['username'],
        password=config['reddit']['password']
    )

    # Function to take a screenshot of a specific HTML element
    def take_screenshot(html_content, output_image, element_class):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.set_content(html_content)

            # Define the selector for the comment div
            comment_selector = f".{element_class}"
            
            # Wait for the element to be present
            page.wait_for_selector(comment_selector, timeout=1000)  # Adjust the timeout as needed

            # Take a screenshot of the specified element
            comment_element = page.locator(comment_selector)
            comment_element.screenshot(path=output_image)
            
            browser.close()

    # Combined function to generate authors, comments, and update HTML
    def update_html_with_authors_and_comments(post_id, comment_urls, title_comments):
        try:
            # Fetch the Reddit submission (post)
            submission = reddit.submission(id=post_id)
            
            # Extract the title author's name
            title_author = submission.author.name if submission.author else "Deleted Account"
            
            # Prepare arrays to store authors and titles/comments
            authors = [title_author]  # Start with the post author's name

            # Loop through each comment URL to extract the comment author
            for url in comment_urls:
                comment_id = url.split('/')[-2]  # Extract the comment ID from the URL
                try:
                    comment = reddit.comment(id=comment_id)
                    comment_author = comment.author.name if comment.author else "Deleted Account"
                    authors.append(comment_author)  # Add comment author to the list
                except Exception as e:
                    print(f"Error retrieving comment ID {comment_id}: {e}")
                    authors.append("Unknown Author")  # Append a placeholder if there's an error

            # Ensure that title_comments is not empty and adjust if necessary
            if not title_comments:
                title_comments = ["No comments available"]

            # Update the HTML file for title
            with open('templates/title.html', 'r') as file:
                soup = BeautifulSoup(file, 'html.parser')

            # Update the author and title in the HTML using BeautifulSoup
            author_element = soup.find(id="author")
            if author_element and len(authors) > 0:
                author_element.string = authors[0]  # Update with the first author (post author)
            
            title_element = soup.find(id="title")
            if title_element and len(title_comments) > 0:
                title_element.string = title_comments[0]  # Update with the first comment (post title)

            # Save the updated HTML for the title
            updated_html_file = 'templates/updated_title.html'
            with open(updated_html_file, 'w') as file:
                file.write(str(soup))
            
            # Take a screenshot of the updated title HTML
            take_screenshot(open(updated_html_file).read(), 'assets/screenshots/screenshot_1.png', 'comment')

            # Ensure both lists have the same length to avoid index errors
            if len(title_comments) - 1 != len(authors) - 1:
                raise ValueError("The length of title_comments and authors lists do not match.")

            # Now update the HTML file for each comment starting from index 1
            for i, (comment, author) in enumerate(zip(title_comments[1:], authors[1:]), start=1):  # Skip the 0th element
                # Load the existing HTML file for each comment
                with open('templates/title.html', 'r') as file:
                    soup = BeautifulSoup(file, 'html.parser')

                # Update the title element with the current comment
                title_element = soup.find(id="title")
                if title_element:
                    title_element.string = comment

                # Update the author element with the current comment
                author_element = soup.find(id="author")
                if author_element and len(authors) > 0:
                    author_element.string = author

                # Save the updated HTML for the comment
                updated_html_file = f'templates/updated_comment_{i}.html'
                with open(updated_html_file, 'w') as file:
                    file.write(str(soup))

                # Take a screenshot of the updated comment HTML
                take_screenshot(open(updated_html_file).read(), f'assets/screenshots/screenshot_{i+1}.png', 'comment')

                # Delete the HTML file after screenshot
                os.remove(updated_html_file)

            # Also delete the title HTML file after screenshot
            os.remove('templates/updated_title.html')

        except Exception as e:
            print("An error occurred while updating the HTML:", e)

# Example usage
post_id = '1eryb78'
comment_urls = [
    'https://www.reddit.com/r/AskReddit/comments/1eryb78/whats_a_sexual_activity_that_seems_exciting_but/li22tpu/',
    'https://www.reddit.com/r/AskReddit/comments/1eryb78/whats_a_sexual_activity_that_seems_exciting_but/li1z1oa/',
    'https://www.reddit.com/r/AskReddit/comments/1eryb78/whats_a_sexual_activity_that_seems_exciting_but/li27bk5/',
    'https://www.reddit.com/r/AskReddit/comments/1eryb78/whats_a_sexual_activity_that_seems_exciting_but/li20d26/',
    'https://www.reddit.com/r/AskReddit/comments/1eryb78/whats_a_sexual_activity_that_seems_exciting_but/li1wp67/',
    'https://www.reddit.com/r/AskReddit/comments/1eryb78/whats_a_sexual_activity_that_seems_exciting_but/li20zeh/',
    'https://www.reddit.com/r/AskReddit/comments/1eryb78/whats_a_sexual_activity_that_seems_exciting_but/li23wui/',
    'https://www.reddit.com/r/AskReddit/comments/1eryb78/whats_a_sexual_activity_that_seems_exciting_but/li1wrtq/',
    'https://www.reddit.com/r/AskReddit/comments/1eryb78/whats_a_sexual_activity_that_seems_exciting_but/li1zgi2/',
    'https://www.reddit.com/r/AskReddit/comments/1eryb78/whats_a_sexual_activity_that_seems_exciting_but/li23xbz/'
]
title_comments = [
    'What’s a sexual activity that seems exciting but often turns out to be less enjoyable than anticipated?',
    'Sex by a river or lake. Mosquitoes on your sack is not an enjoyable experience.',
    'Sex on the beach. Sand, so much sand.',
    'Sex in nature. Bugs and mosquitoes eat you alive.',
    'Sex with your roommates girlfriend.',
    'Shower sex',
    'Threesomes with a person you love.',
    'Sex of any kind in a body of water from a bath tub to an ocean',
    'Having a big boner then losing it',
    'Anything in a car.'
]

# Call the function to update HTML and take screenshots
# update_html_with_authors_and_comments(post_id, comment_urls, title_comments)