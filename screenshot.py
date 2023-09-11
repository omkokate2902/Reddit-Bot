import praw
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from PIL import Image
import os

# Reddit API credentials
reddit = praw.Reddit(
    client_id="I4ZRQ8ZE7Cpz8tkbpdCp5A",
    client_secret="cWVQiNW6S2JgNqHPZT-54_I5_m9B4A",
    user_agent="bot2:v1.0 (by /u/PatientStreet3556)"
)

# Get the post details
post = reddit.submission(id='16fie14')

# Configure Chrome options (optional)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')  # Run Chrome in headless mode (without GUI)

# Create a Chrome driver instance
driver = webdriver.Chrome(options=chrome_options)

# Navigate to the Reddit post URL
driver.get(post.url)

# Capture a screenshot
driver.save_screenshot('assets/screenshots/reddit_post_screenshot.png')

# Load the screenshot using Pillow
screenshot = Image.open('assets/screenshots/reddit_post_screenshot.png')

# Define the coordinates to crop the question and username
# You'll need to adjust these coordinates based on the specific layout of the Reddit post page
left = 0  # Adjust this value as needed
top = 150   # Adjust this value as needed
right = 850  # Adjust this value as needed
bottom = 500  # Adjust this value as needed

# Crop the screenshot
cropped_image = screenshot.crop((left, top, right, bottom))

# Save the cropped image
cropped_image.save('assets/screenshots/reddit_question_username.png')

# Delete the original screenshot file if it exists
if os.path.exists('assets/screenshots/reddit_post_screenshot.png'):
    os.remove('assets/screenshots/reddit_post_screenshot.png')

# Close the Chrome driver
driver.quit()
