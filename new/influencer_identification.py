# influencer_identification.py
import pandas as pd

def identify_influencers(authors_df, min_followers=100_000, min_likes=1_000_000):
    try:
        influencers = authors_df[
            (authors_df['follower_count'] >= min_followers) &
            (authors_df['like_count'] >= min_likes)
        ]
        print(f"Identified {len(influencers)} influencers.")
        return influencers
    except Exception as e:
        print(f"Error identifying influencers: {e}")
        return pd.DataFrame()  # Return empty DataFrame on error
