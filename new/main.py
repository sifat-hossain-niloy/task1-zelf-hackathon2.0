# main.py
from scraper import TikTokScraper, human_like_mouse_move
from author_info import AuthorInfoScraper
from influencer_identification import identify_influencers
from data_storage import save_posts, save_authors, save_influencers
from engagement import Engagement
from engagement_verification import EngagementVerification
import pandas as pd
import csv
import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import csv
from selenium_stealth import stealth
import pyautogui


# Define keywords and hashtags
KEYWORDS = [
    "beautiful destinations",
    "places to visit",
    "places to travel",
    "places that don't feel real",
    "travel hacks"
]

HASHTAGS = [
    "#traveltok", "#wanderlust", "#backpackingadventures",
    "#luxurytravel", "#hiddengems", "#solotravel",
    "#roadtripvibes", "#travelhacks", "#foodietravel",
    "#sustainabletravel"
]

# Step 1: Setup a list of user agents for rotation
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
    ' Chrome/58.0.3029.110 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
    ' Chrome/51.0.2704.103 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
    ' Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/605.1.15 (KHTML, like Gecko)'
    ' Version/11.1 Safari/604.5.6',
]

# Step 2: Set up the Selenium WebDriver
def start_driver(user_agent=None):
    service = Service(executable_path=r'D:\Scraping\chromedriver-win64\chromedriver.exe')
    
    # Rotate user agents
    options = webdriver.ChromeOptions()
    if user_agent:
        options.add_argument(f"user-agent={user_agent}")

    # Add additional options if necessary
    options.add_argument("--disable-blink-features=AutomationControlled")  # Prevent detection
    options.add_argument("--start-maximized")
    
    driver = webdriver.Chrome(service=service, options=options)

    # Use Selenium Stealth to avoid detection
    stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )

    return driver

def main():
    # Step 3: Start the browser with a rotating user-agent
    user_agent = random.choice(USER_AGENTS)
    driver = start_driver(user_agent)
    
    # Initialize WebDriverWait for 10 seconds
    wait = WebDriverWait(driver, 10)
    
    # Step 4: Open TikTok's main page
    driver.get('https://www.tiktok.com')
    
    # Allow the page to load
    time.sleep(random.uniform(1, 5))
    
    # Initialize TikTokScraper with driver and wait
    scraper = TikTokScraper(driver=driver, wait=wait)
    
    try:
        # Perform login (commented out as per your request)
        # scraper.login(credentials_file='credentials.txt')

        # Initialize CSV for video data
        with open('tiktok_video_data.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Video URL', 'Text', 'Comments'])

            # Scrape posts based on keywords
            for keyword in KEYWORDS:
                print(f"Searching for keyword: {keyword}")
                scraper.perform_search(keyword)
                video_links = scraper.scrape_video_links()
                print(f"Found {len(video_links)} video links for keyword: {keyword}")
                scraper.scrape_video_data(video_links, writer)

            # Scrape posts based on hashtags
            for hashtag in HASHTAGS:
                print(f"Searching for hashtag: {hashtag}")
                scraper.perform_search(hashtag)
                video_links = scraper.scrape_video_links()
                print(f"Found {len(video_links)} video links for hashtag: {hashtag}")
                scraper.scrape_video_data(video_links, writer)

        print("Video scraping completed.")

        # Read the scraped video data
        df_posts = pd.read_csv('tiktok_video_data.csv')
        save_posts(df_posts.to_dict(orient='records'), filename='posts.csv')

        # Extract unique authors
        unique_usernames = df_posts['Video URL'].apply(lambda x: extract_username_from_url(x)).unique()
        print(f"Unique authors found: {len(unique_usernames)}")

        # Initialize AuthorInfoScraper
        author_scraper = AuthorInfoScraper(driver=driver, wait=wait)
        authors = []
        for idx, username in enumerate(unique_usernames, 1):
            if username:  # Ensure username is not None
                print(f"Collecting info for author {idx}/{len(unique_usernames)}: {username}")
                info = author_scraper.get_author_info(username)
                if info:
                    authors.append(info)

        # Save authors to CSV
        save_authors(authors, filename='authors.csv')

        # Identify influencers
        authors_df = pd.DataFrame(authors)
        influencers = identify_influencers(authors_df)
        save_influencers(influencers, filename='influencers.csv')

        print("Influencer identification completed.")

        # Bonus Features: Engagement
        engage = Engagement(driver=driver, wait=wait)
        verification = EngagementVerification(driver=driver, wait=wait, username='your_username')  # Replace with your TikTok username

        # Example: Like and comment on the first influencer's video
        if not influencers.empty:
            top_influencer = influencers.iloc[0]
            influencer_username = top_influencer['username']
            influencer_profile_url = f"https://www.tiktok.com/@{influencer_username}"
            print(f"Engaging with influencer: {influencer_username}")

            # Assuming you have a way to get the influencer's video URL
            # For demonstration, using the first video link from influencer's profile
            scraper.driver.get(influencer_profile_url)
            time.sleep(random.uniform(2, 5))
            influencer_video_links = scraper.scrape_video_links()
            if influencer_video_links:
                video_url = influencer_video_links[0]
                engage.like_video(video_url)
                engage.comment_video(video_url, "Great content!")
                # Verify the comment
                is_verified = verification.verify_comment(video_url, "Great content!")
                print(f"Comment verification: {'Success' if is_verified else 'Failure'}")
            else:
                print(f"No videos found for influencer: {influencer_username}")

    except Exception as e:
        print(f"An error occurred in main: {e}")

    finally:
        driver.quit()
        print("Scraping process completed.")

def extract_username_from_url(video_url):
    # Extract username from video URL, e.g., https://www.tiktok.com/@username/video/123456789
    try:
        parts = video_url.split('/')
        username = parts[3].replace('@', '')
        return username
    except:
        return None

if __name__ == "__main__":
    main()
