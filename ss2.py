from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService


# Initialize the WebDriver
driver = webdriver.Chrome(executable_path='/Users/omkokate/Desktop/reddit_bot/myenv/lib/python3.10/site-packages/selenium/webdriver/chromium')

# Navigate to the web page
driver.get('https://www.reddit.com/r/AskReddit/comments/16fz24y/what_is_your_favorite_sport/')  # Replace with the URL of the web page you want to capture

# Specify the text content you want to locate
target_text = "Rugby, because it's like football, but for people who can't afford pads."

try:
    # Use XPath to locate the element by its text content
    comment_element = driver.find_element(By.XPATH, f'//*[contains(text(), "{target_text}")]')

    # Scroll the comment element into view
    driver.execute_script("arguments[0].scrollIntoView();", comment_element)

    # Capture a screenshot of the element
    comment_screenshot = comment_element.screenshot_as_png

    # Save the screenshot to a file
    with open('comment.png', 'wb') as screenshot_file:
        screenshot_file.write(comment_screenshot)

    print("Screenshot captured and saved successfully!")

except Exception as e:
    print(f"An error occurred: {str(e)}")

finally:
    # Close the WebDriver
    driver.quit()