from playwright.sync_api import sync_playwright, ViewportSize
import os

def capture_screenshots(post_url, comment_urls, output_folder):

    chromium_executable_path = './opt/homebrew/bin/chromium'

    # Set the PW_BROWSER_PATH environment variable to the Chromium path
    os.environ['PW_BROWSER_PATH'] = chromium_executable_path

    with sync_playwright() as p:
        # Launch a headless Chromium browser
        browser = p.chromium.launch(headless=True)

        # Create a new browser context with a specific viewport size
        context = browser.new_context(viewport=ViewportSize(width=1920, height=1080))

        # Create a new page in the context
        page = context.new_page()

        try:
            # Navigate to the Reddit post URL
            page.goto(post_url)

            # Capture a screenshot of the post title
            title_screenshot_path = f"{output_folder}/title.png"
            title_element = page.locator('your_selector_for_title_element')
            title_element.screenshot(path=title_screenshot_path)

            # Iterate through comment URLs and capture screenshots
            for index, comment_url in enumerate(comment_urls, start=1):
                page.goto(comment_url)

                # Capture a screenshot of the comment
                comment_screenshot_path = f"{output_folder}/comment_{index}.png"
                comment_element = page.locator('your_selector_for_comment_element')
                comment_element.screenshot(path=comment_screenshot_path)

        finally:
            # Close the browser to release resources
            browser.close()

# Example usage:
if __name__ == "__main__":
    post_url = "https://www.reddit.com/r/subreddit/comments/post_id/"
    comment_urls = [
        "https://www.reddit.com/r/subreddit/comments/post_id/comment/comment_id1/",
        "https://www.reddit.com/r/subreddit/comments/post_id/comment/comment_id2/",
        # Add more comment URLs as needed
    ]
    output_folder = "assets/screenshots"

    # Call the function to capture screenshots
    capture_screenshots(post_url, comment_urls, output_folder)
