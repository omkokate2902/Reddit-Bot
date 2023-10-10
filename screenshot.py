from playwright.sync_api import sync_playwright, ViewportSize
from PIL import Image

def capture_screenshots(post_id,post_url, comment_urlss):
    output_folder="assets/screenshots"
    post_id=post_id
    
    prefix = "https://publish.reddit.com/embed?url="

    comment_urls = [f"{prefix}{url}" for url in comment_urlss]

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
            title_element = page.locator(f'#t3_{post_id}')
            title_element.screenshot(path=title_screenshot_path)

            print("Captured title screenshot...\n")

            # Iterate through comment URLs and capture screenshots
            for index, comment_url in enumerate(comment_urls, start=1):
                page.goto(comment_url)

                # Wait for 5 seconds to allow the page to load comments
                page.wait_for_timeout(5000)  # Wait for 5 seconds

                # Capture a screenshot of the comment
                comment_screenshot_path = f"{output_folder}/comment_{index}.png"
                comment_id = 'preview_block'  # Replace with the actual 'id' of the comment div
                comment_selector = f'#{comment_id}'
                page.wait_for_selector(comment_selector, timeout=10000)  # Adjust the timeout as needed
                comment_element = page.locator(comment_selector)
                comment_element.screenshot(path=comment_screenshot_path)

                # Open the captured screenshot with PIL
                image = Image.open(comment_screenshot_path)

                crop_rect = (0, 0, image.width, image.height - 50)
                cropped_image = image.crop(crop_rect)

                cropped_image.save(comment_screenshot_path)
                
                print(f"Captured comment_{index} screenshot...\n")



        finally:
            # Close the browser to release resources
            browser.close()
