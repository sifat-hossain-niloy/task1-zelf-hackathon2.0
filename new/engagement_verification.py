# engagement_verification.py
import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class EngagementVerification:
    def __init__(self, driver, wait, username):
        self.driver = driver
        self.wait = wait
        self.username = username

    def verify_comment(self, video_url, comment_text):
        try:
            self.driver.get(video_url)
            self.random_delay(2, 5)

            # Scroll to load comments
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.random_delay(2, 4)

            # # Locate all comments
            # comment_elements = self.wait.until(EC.presence_of_all_elements_located(
            #     (By.XPATH, '//div[contains(@class,"comment-content")]')))  # Replace with actual XPath

            # for comment in comment_elements:
            #     try:
            #         author = comment.find_element(By.XPATH, './/span[contains(@class,"comment-user")]').text  # Replace with actual XPath
            #         text = comment.find_element(By.XPATH, './/p').text  # Replace with actual XPath
            #         if author.lower() == self.username.lower() and text == comment_text:
            #             print(f"Comment verified: {comment_text}")
            #             return True
            #     except:
            #         continue
            # print("Comment verification failed.")
            # return False

        except Exception as e:
            print(f"Error verifying comment on {video_url}: {e}")
            return False

    def random_delay(self, min_seconds=2, max_seconds=5):
        time.sleep(random.uniform(min_seconds, max_seconds))
