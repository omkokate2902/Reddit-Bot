from playwright.sync_api import sync_playwright, ViewportSize

def capture_screenshots(post_url, comment_urls, output_folder):
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

            # Check if the NSFW button is visible and click it if necessary
            nsfw_button_selector = 'your_selector_for_nsfw_button'
            if page.locator(nsfw_button_selector).is_visible():
                print("NSFW content detected. Clicking the NSFW button...")
                page.locator(nsfw_button_selector).click()
                page.wait_for_load_state()  # Wait for the page to fully load again

            # Capture a screenshot of the post title
            title_screenshot_path = f"{output_folder}/title.png"
            title_element = page.locator('#t3_16wtqch')
            title_element.screenshot(path=title_screenshot_path)

            # Iterate through comment URLs and capture screenshots
            for index, comment_url in enumerate(comment_urls, start=1):
                page.goto(comment_url)

                # Capture a screenshot of the comment
                comment_screenshot_path = f"{output_folder}/comment_{index}.png"
                comment_element = page.locator('#t3_12hmbug > div > div._3xX726aBn29LDbsDtzr_6E._1Ap4F5maDtT1E1YuCiaO0r.D3IL3FD0RFy_mkKLPwL4 > div > div > button')

                comment_element.screenshot(path=comment_screenshot_path)

        finally:
            # Close the browser to release resources
            browser.close()

# Example usage:
if __name__ == "__main__":
    post_url = "https://www.reddit.com/r/AskReddit/comments/16wtqch/men_who_suddenly_lost_your_interest_in_someone"
    comment_urls = [
        "https://www.reddit.com/r/AskReddit/comments/16wtqch/men_who_suddenly_lost_your_interest_in_someone/k2z3cgf",
        "https://www.reddit.com/r/AskReddit/comments/16wtqch/men_who_suddenly_lost_your_interest_in_someone/k2yxli8",
        # Add more comment URLs as needed
    ]
    output_folder = "assets/screenshots"

    # Call the function to capture screenshots
    capture_screenshots(post_url, comment_urls, output_folder)
