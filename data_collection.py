#------ Real-time Data Collection with time&pd&Vader Libraries ------#

import praw
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os
import time
import random

# Initialize Reddit API client
reddit = praw.Reddit(
    client_id="NT6xR6Qm2X_GT9uI-tnU0w",
    client_secret="ctNQXy_6K81LrZ8szunwDLnhHJQvOQ",
    user_agent="East-Assumption691"
)

# Initialize VADER sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Queries for fetching posts
queries = [
    "global warming", "greenhouse gases", "carbon emissions",
    "extreme weather", "carbon intensity", "biodiversity",
    "carbon footprint", "climate crisis", "carbon market",
    "cutting down forests", "powering buildings", "manufacturing goods",
    "fossil fuels"
]

# Sorting options to ensure variety in the fetched data
sort_options = ["top", "comments", "relevance"]

# Function to classify sentiment
def classify_sentiment(text):
    scores = analyzer.polarity_scores(str(text))  # Convert to string to handle NaN
    if scores['compound'] >= 0.05:
        return "Positive"
    elif scores['compound'] <= -0.05:
        return "Negative"
    else:
        return "Neutral"

# Function to fetch data iteratively from Reddit
def fetch_data(subreddit_name, min_rows=600, batch_size=100, cycle=0, max_attempts=10):
    posts = []
    seen_ids = set()  # Track unique post IDs to avoid duplicates
    subreddit = reddit.subreddit(subreddit_name)
    attempts = 0

    print(f"Starting fetch for at least {min_rows} rows of data...")

    while len(posts) < min_rows and attempts < max_attempts:
        sort_order = sort_options[cycle % len(sort_options)]
        shuffled_queries = random.sample(queries, len(queries))
        print(f"Attempt {attempts + 1}: Fetching data...")

        for query in shuffled_queries:
            print(f"Searching for query: {query} (sort: {sort_order})")
            for submission in subreddit.search(query, sort=sort_order, limit=batch_size):
                # Skip duplicates or invalid selftexts
                if (
                    submission.id in seen_ids
                    or not submission.selftext
                    or pd.isna(submission.selftext)
                    or submission.selftext.strip() == ""
                ):
                    continue
                seen_ids.add(submission.id)
                post = {
                    "id": submission.id,
                    "title": submission.title,
                    "selftext": submission.selftext,
                    "created_utc": submission.created_utc,
                    "score": submission.score,
                    "comments": submission.num_comments,
                    "url": submission.url,
                    "query": query,  # Track the query that retrieved this post
                    # Apply sentiment analysis
                    "selftext_sentiment": classify_sentiment(submission.selftext)
                }
                posts.append(post)
                if len(posts) % 50 == 0:  # Show progress every 50 posts
                    print(f"Progress: {len(posts)} rows collected...")

            if len(posts) >= min_rows:
                print(f"Collected {len(posts)} rows. Stopping further queries.")
                break

        attempts += 1
        cycle += 1  # Rotate the sort order for variety

    if len(posts) < min_rows:
        print(f"Warning: Only {len(posts)} rows fetched after {attempts} attempts.")

    return pd.DataFrame(posts).drop_duplicates(subset="id")  # Remove duplicates by post ID

# Function to replace CSV data and update sentiment analysis
def replace_csv(output_file, new_data):
    # Save new data directly
    new_data.to_csv(output_file, index=False)
    print(f"Replaced CSV file with {len(new_data)} rows.")

    # Print sentiment distribution
    sentiment_counts = new_data['selftext_sentiment'].value_counts()
    print("\nSentiment Analysis Distribution (Updated):")
    print(f"Positive: {sentiment_counts.get('Positive', 0)}")
    print(f"Neutral: {sentiment_counts.get('Neutral', 0)}")
    print(f"Negative: {sentiment_counts.get('Negative', 0)}")

# Main function to continuously fetch and replace data
def collect_data_continuously(subreddit_name, output_file="data.csv", batch_size=100, fetch_interval=60, min_rows=600):
    print(f"Starting continuous data collection and saving to {output_file}.")
    cycle = 0  # Counter to alternate sorting order and ensure variety

    while True:
        # Fetch fresh data for each cycle
        new_data = fetch_data(subreddit_name, min_rows, batch_size, cycle)

        # Replace the old data with new data
        if not new_data.empty:
            replace_csv(output_file, new_data)
        else:
            print("No valid data found.")

        # Increment the cycle for alternating sort
        cycle += 1

        # Wait before fetching new data
        print(f"Waiting {fetch_interval} seconds before fetching new data...\n")
        time.sleep(fetch_interval)

# Start the data collection process
subreddit_name = "climatechange"  # Target subreddit
output_csv = "data.csv"
batch_size = 100                  # Number of posts to fetch per query
fetch_interval = 60               # Time in seconds between each fetch
min_rows = 600                    # Minimum rows in the CSV file

collect_data_continuously(subreddit_name, output_csv, batch_size, fetch_interval, min_rows)
