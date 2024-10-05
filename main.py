from helpers import fetch_video_data

# Main function to execute the scraping process
def execute_scraping():
    keywords = ['beautiful destinations',   
                'places to visit',
                'places to travel',
                "places that don't feel real",
                'travel hacks']
    
    hashtags = ['traveltok',
                'wanderlust',
                'backpackingadventures',
                'luxurytravel',
                'hiddengems',
                'solotravel',
                'roadtripvibes',
                'travelhacks',
                'foodietravel',
                'sustainabletravel']
    
    # Call the function to fetch video data
    fetch_video_data(keywords, hashtags)

if __name__ == "__main__":
    execute_scraping()
