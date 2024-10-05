# data_storage.py
import pandas as pd

def save_posts(posts, filename='posts.csv'):
    try:
        df = pd.DataFrame(posts)
        df.to_csv(filename, index=False)
        print(f"Saved posts to {filename}.")
    except Exception as e:
        print(f"Error saving posts to {filename}: {e}")

def save_authors(authors, filename='authors.csv'):
    try:
        df = pd.DataFrame(authors)
        df.to_csv(filename, index=False)
        print(f"Saved authors to {filename}.")
    except Exception as e:
        print(f"Error saving authors to {filename}: {e}")

def save_influencers(influencers, filename='influencers.csv'):
    try:
        influencers.to_csv(filename, index=False)
        print(f"Saved influencers to {filename}.")
    except Exception as e:
        print(f"Error saving influencers to {filename}: {e}")
