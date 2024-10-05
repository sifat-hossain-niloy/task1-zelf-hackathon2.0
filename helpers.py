import time
import pandas as pd
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def fetch_video_data(search_terms, hashtags):
    driver_path = "/usr/local/bin/geckodriver"
    browser_options = Options()
    browser_options.set_preference('profile', driver_path)
    driver = Firefox(options=browser_options)
    
    scraped_data = []
    
    # Fetch data for search terms
    for term in search_terms:
        search_url = f"https://www.tiktok.com/search?lang=en&q={term}&t=1718069674294"
        driver.get(search_url)
        time.sleep(10)
        perform_scroll(driver)

        video_links = [element.get_attribute('href') for element in 
                 driver.find_elements(By.CLASS_NAME, 'css-1g95xhm-AVideoContainer.e19c29qe13')]
        
        creators_1 = [creator.text for creator in driver.find_elements(By.CLASS_NAME, 'css-2zn17v-PUniqueId.etrd4pu6')]
        video_captions = [text.text for text in driver.find_elements(By.CLASS_NAME, 'css-6opxuj-H1Container.ejg0rhn1')]

        scraped_data.append({
            'video_url': video_links,
            'creators': creators_1,
            'captions': video_captions
        })
    
    # Fetch data for hashtags
    for tag in hashtags:
        hashtag_url = f"https://www.tiktok.com/tag/{tag}"
        print(hashtag_url)
        
        driver.get(hashtag_url)
        time.sleep(30)
        perform_scroll(driver)

        hashtag_video_links = [element.get_attribute('href') for element in 
                 driver.find_elements(By.CLASS_NAME, 'css-1g95xhm-AVideoContainer.e19c29qe13')]
        hashtag_captions = [text.text for text in 
                    driver.find_elements(By.CLASS_NAME, "css-1wrhn5c-AMetaCaptionLine.eih2qak0")]
        creators_2 = [creator.text for creator in 
                        driver.find_elements(By.CLASS_NAME, "user-name.css-1gi42ki-PUserName.exdlci15")]

        scraped_data.append({
            'video_url': hashtag_video_links,
            'creators': creators_2,
            'captions': hashtag_captions
        })

        result_df = pd.DataFrame(data=scraped_data, columns=scraped_data[0].keys())
        result_df.to_csv('tiktok_scraped_data.csv', index=False)
    
    scrape_profile_data(driver, creators_1 + creators_2)
    driver.quit()


def scrape_profile_data(driver, creator_list):
    profile_data = []

    for creator in creator_list:
        profile_url = f"https://www.tiktok.com/@{creator}"
        driver.get(profile_url)
        time.sleep(2)

        user_name_list = [user.text for user in driver.find_elements(By.CLASS_NAME, "css-11ay367-H1ShareTitle.e1457k4r8")]
        print(user_name_list)
        stats = [stat.text for stat in driver.find_elements(By.CLASS_NAME, "css-1ldzp5s-DivNumber.e1457k4r1")]
        following_count, follower_count = stats[0].split("\n")[0], stats[1].split("\n")[0]
        total_likes = [like.text for like in 
                driver.find_elements(By.CLASS_NAME, "css-pmcwcg-DivNumber.e1457k4r1")][0].split("\n")[0]
        
        profile_data.append({
            'user_name': user_name_list,
            'following_count': following_count,
            'follower_count': follower_count,
            'total_likes': total_likes
        })

        profile_df = pd.DataFrame(data=profile_data, columns=profile_data[0].keys())
        profile_df.to_csv('creator_profile_data.csv', index=False)


def perform_scroll(driver):
    """A helper function to automate scrolling."""

    last_position = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)

        new_position = driver.execute_script("return document.body.scrollHeight")
        if new_position == last_position:
            break
        last_position = new_position
