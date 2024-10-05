from selenium.webdriver.support import expected_conditions as EC

# Load the CSV file with the modified file name
data_frame = pd.read_csv('tiktok_scraped_data.csv')

# Print the number of authors
print(len(data_frame['creators'].tolist()))

# Iterate through the list of creators and print the first character of each
for creator in data_frame['creators'].tolist():
    print(creator[0])
