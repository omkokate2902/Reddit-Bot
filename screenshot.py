from playwright.sync_api import sync_playwright, ViewportSize
import os

def capture_screenshots(post_url, comment_urls, output_folder):

    chromium_executable_path = './opt/homebrew/Caskroom/chromium/latest'

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
            title_element = page.locator('#t3_16wa47t')
            title_element.screenshot(path=title_screenshot_path)

            # Iterate through comment URLs and capture screenshots
            for index, comment_url in enumerate(comment_urls, start=1):
                page.goto(comment_url)

                # Capture a screenshot of the comment
                comment_screenshot_path = f"{output_folder}/comment_{index}.png"
                comment_element = page.locator('#t1_k2xck8k > div.Comment.t1_k2xck8k.P8SGAKMtRxNwlmLz1zdJu.HZ-cv9q391bm8s7qT54B3._1z5rdmX8TDr6mqwNv7A70U')
                
                comment_element.screenshot(path=comment_screenshot_path)

        finally:
            # Close the browser to release resources
            browser.close()

# Example usage:
if __name__ == "__main__":
    post_url = "https://www.reddit.com/r/AskReddit/comments/16wa47t/whats_something_common_that_men_do_that_women/"
    comment_urls = [
        "https://www.reddit.com/r/AskReddit/comments/16wa47t/whats_something_common_that_men_do_that_women/",
        "https://www.reddit.com/r/AskReddit/comments/16wa47t/whats_something_common_that_men_do_that_women/",
        # Add more comment URLs as needed
    ]
    output_folder = "assets/screenshots"

    # Call the function to capture screenshots
    capture_screenshots(post_url, comment_urls, output_folder)
