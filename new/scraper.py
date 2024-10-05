# scraper.py
import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pyautogui

# Simulate moving the mouse to a random position before clicking
def human_like_mouse_move(driver, element):
    location = element.location
    size = element.size
    x = location['x'] + random.uniform(0, size['width'])
    y = location['y'] + random.uniform(0, size['height'])
    pyautogui.moveTo(x, y, duration=random.uniform(0.5, 2))  # Move to the element slowly

class TikTokScraper:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def perform_search(self, query):
        try:
            # Click on the search input
            search_input = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="app-header"]/div/div[2]/div/form/input')))  # Replace with actual XPath
            human_like_mouse_move(self.driver, search_input)
            search_input.click()
            self.random_delay()

            # Enter the search query
            search_input.send_keys(query)
            self.random_delay()

            # Submit the search
            search_input.submit()
            self.random_delay()
            print(f"Searched for: {query}")

            # Allow time for search results to load
            self.random_delay(3, 6)
        except Exception as e:
            print(f"Error performing search for '{query}': {e}")

    def scrape_video_links(self, max_videos=10):
        """
        Scrapes video links from the current search results page.

        Args:
            max_videos (int): The maximum number of video links to scrape.

        Returns:
            list: A list of scraped video URLs.
        """
        video_links = []
        try:
            while len(video_links) < max_videos:
                # Wait until video elements are present
                videos = self.wait.until(EC.presence_of_all_elements_located(
                    (By.XPATH, '//a[contains(@href, "/@") and contains(@href, "/video/")]')))  # Replace with actual XPath

                for video in videos:
                    if len(video_links) >= max_videos:
                        break  # Stop if we've reached the maximum number of videos

                    link = video.get_attribute('href')
                    if link and link not in video_links:
                        video_links.append(link)
                        print(f"Scraped video link: {link}")
                
                print(f"Total scraped video links: {len(video_links)}")
                
                if len(video_links) < max_videos:
                    # Scroll down to load more videos
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    self.random_delay(2, 4)
                else:
                    break

        except Exception as e:
            print(f"Error scraping video links: {e}")
        return video_links

    def scrape_video_data(self, video_links, writer):
        for link in video_links:
            try:
                self.driver.get(link)
                self.random_delay(2, 5)

                # Scrape the video description or text
                video_text_element = self.wait.until(EC.visibility_of_element_located(
                    (By.XPATH, '//div[contains(@class,"video-meta-title")]/h1')))  # Replace with actual XPath
                video_text = video_text_element.text
                print(f"Video Text: {video_text}")

                # Scrape all comments
                comments = []
                # Scroll to load comments
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                self.random_delay(2, 4)
                comment_elements = self.driver.find_elements(By.XPATH, '//div[contains(@class,"comment-content")]/p')  # Replace with actual XPath
                for comment_element in comment_elements:
                    comment_text = comment_element.text
                    comments.append(comment_text)
                    print(f"Comment: {comment_text}")

                # Write the video URL, description, and comments to CSV
                writer.writerow([link, video_text, " | ".join(comments)])

            except Exception as e:
                print(f"Error scraping video data from {link}: {e}")
                continue  # Move to the next video if there's an error

    def random_delay(self, min_seconds=2, max_seconds=5):
        time.sleep(random.uniform(min_seconds, max_seconds))
