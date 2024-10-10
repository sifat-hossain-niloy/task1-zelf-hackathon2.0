import time
import json
import pandas as pd
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


def init_webdriver(webdriver_path):
    options = webdriver.ChromeOptions()
    service = Service(executable_path=webdriver_path)
    options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
    driver = webdriver.Chrome(options=options, service=service)
    return driver


# Function to get the JSON response directly using Selenium
def get_json_response_from_api(driver, api_url):
    driver.get(api_url)
    time.sleep(5)  # Wait for the page to load (adjust based on the page)
    
    # Retrieve the full page source after loading (assuming JSON is loaded in the body)
    body_text = driver.find_element(By.TAG_NAME, 'body').text
    
    try:
        # Parse the text as JSON if it's valid JSON
        json_data = json.loads(body_text)
        return json_data
    except json.JSONDecodeError:
        print("Failed to decode JSON from the response.")
        return None


def extract_logs(driver):
    """Extract performance logs from the browser."""
    logs_raw = driver.get_log("performance")
    return [json.loads(lr["message"])["message"] for lr in logs_raw]


def filter_logs(logs, search_string):
    """Filter logs to find specific responses based on a search string."""
    def log_filter(log_):
        return (
            log_["method"] == "Network.responseReceived" and
            "json" in log_["params"]["response"]["mimeType"] and
            search_string in log_["params"]["response"]["url"]
        )
    return filter(log_filter, logs)


def process_logs(driver, logs, search_string):
    """Process logs to retrieve response data and save matched URLs in a list."""
    matched_urls = []
    for log in filter_logs(logs, search_string):
        request_id = log["params"]["requestId"]
        resp_url = log["params"]["response"]["url"]
        # print(f"Matched {search_string} in URL: {resp_url}")
        matched_urls.append(resp_url)  # Add matched URL to the list
    return matched_urls  # Return the list of matched URLs


def scroll_down(driver):
    """Scroll down to the bottom of the page."""
    last_height = driver.execute_script("return document.body.scrollHeight")
    it = 0
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(12 if it == 0 else 5)
        it += 1
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def search_by_keyword(driver, search_inputs, search_string):
    """Search TikTok by keyword and extract logs."""
    all_matched_urls = []
    for kw in search_inputs:
        url = f"https://www.tiktok.com/search?lang=en&q={kw}&t=1728099684294"
        driver.get(url)
        time.sleep(5)
        scroll_down(driver)
        logs = extract_logs(driver)
        matched_urls = process_logs(driver, logs, search_string)
        all_matched_urls.extend(matched_urls)  # Append all matched URLs to a common list
    return all_matched_urls


def search_by_hashtag(driver, hash_tags, search_tag):
    """Search TikTok by hashtag and extract logs."""
    all_matched_urls = []
    for tag in hash_tags:
        url = f"https://www.tiktok.com/tag/{tag}"
        driver.get(url)
        time.sleep(5)
        scroll_down(driver)
        logs = extract_logs(driver)
        matched_urls = process_logs(driver, logs, search_tag)
        all_matched_urls.extend(matched_urls)  # Append all matched URLs to a common list
    return all_matched_urls


def get_searched_links(search_inputs, hash_tags):
    webdriver_path = r'D:\Scraping\task1-zelf-hackathon2.0\chromedriver-win64\chromedriver.exe'
    search_string = "full/?WebIdLastTime="
    search_tag = "api/challenge/item_list/?WebIdLastTime="
    
    # Initialize driver
    driver = init_webdriver(webdriver_path)
    
    # Search using keywords
    keyword_urls = search_by_keyword(driver, search_inputs, search_string)
    
    # Search using hashtags
    hashtag_urls = search_by_hashtag(driver, hash_tags, search_tag)
    
    
    # Combine all URLs and return
    all_urls = keyword_urls + hashtag_urls
    # Flag to control header writing
    write_header = True

    for url in all_urls:
        data = get_json_response_from_api(driver, url)
        
        # Normalize the JSON data and convert to a DataFrame
        df = pd.json_normalize(data.get('data'))
        
        # List of columns to keep
        columns_to_keep = [
            'item.desc',
            'item.author.nickname',
            'item.authorStats.followingCount',
            'item.authorStats.followerCount',
            'item.authorStats.heartCount'
        ]
        
        # Filter the DataFrame to only include the specified columns
        df_filtered = df[columns_to_keep]
        
        # Append to CSV, only writing the header for the first batch
        df_filtered.to_csv("videos+authors.csv", mode='a', header=write_header, index=False)
        
        # After the first iteration, don't write the header again
        write_header = False    
    driver.quit()
    
    
    


