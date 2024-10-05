# author_info.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class AuthorInfoScraper:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def get_author_info(self, username):
        profile_url = f"https://www.tiktok.com/@{username}"
        try:
            self.driver.get(profile_url)
            self.random_delay(2, 5)

            # Scrape follower count
            follower_element = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="main-content-others_homepage"]/div/div[1]/div[2]/div[3]/h3/div[2]/strong')))  # Replace with actual XPath
            follower_count = follower_element.text

            # Scrape following count
            following_element = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="main-content-others_homepage"]/div/div[1]/div[2]/div[3]/h3/div[1]/strong')))  # Replace with actual XPath
            following_count = following_element.text

            # Scrape like count
            like_element = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="main-content-others_homepage"]/div/div[1]/div[2]/div[3]/h3/div[2]/strong')))  # Replace with actual XPath
            like_count = like_element.text

            author_info = {
                'username': username,
                'follower_count': self.parse_count(follower_count),
                'following_count': self.parse_count(following_count),
                'like_count': self.parse_count(like_count)
            }
            print(f"Collected info for {username}: {author_info}")
            return author_info

        except Exception as e:
            print(f"Error collecting author info for {username}: {e}")
            return None

    def parse_count(self, count_str):
        count_str = count_str.strip()
        try:
            if 'K' in count_str:
                return int(float(count_str.replace('K', '').replace(',', '')) * 1_000)
            elif 'M' in count_str:
                return int(float(count_str.replace('M', '').replace(',', '')) * 1_000_000)
            else:
                return int(count_str.replace(',', ''))
        except:
            return 0

    def random_delay(self, min_seconds=2, max_seconds=5):
        time.sleep(random.uniform(min_seconds, max_seconds))
