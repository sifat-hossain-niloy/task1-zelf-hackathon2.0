# engagement.py
import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class Engagement:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def like_video(self, video_url):
        try:
            self.driver.get(video_url)
            self.random_delay(2, 5)

            # Click the like button
            like_button = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//button[contains(@aria-label, "Like")]')))  # Replace with actual XPath
            human_like_mouse_move(self.driver, like_button)
            like_button.click()
            print(f"Liked the video: {video_url}")
            self.random_delay(1, 3)
        except Exception as e:
            print(f"Error liking video {video_url}: {e}")

    def comment_video(self, video_url, comment_text):
        try:
            self.driver.get(video_url)
            self.random_delay(2, 5)

            # Click on the comment box
            comment_box = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//textarea[@placeholder="Add a comment..."]')))  # Replace with actual XPath
            human_like_mouse_move(self.driver, comment_box)
            comment_box.click()
            self.random_delay(1, 2)

            # Enter the comment
            comment_box.send_keys(comment_text)
            self.random_delay(1, 2)

            # Submit the comment
            submit_button = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//button[@data-e2e="comment-submit"]')))  # Replace with actual XPath
            human_like_mouse_move(self.driver, submit_button)
            submit_button.click()
            print(f"Posted comment on video: {video_url}")
            self.random_delay(1, 3)
        except Exception as e:
            print(f"Error commenting on video {video_url}: {e}")

    def random_delay(self, min_seconds=2, max_seconds=5):
        time.sleep(random.uniform(min_seconds, max_seconds))
