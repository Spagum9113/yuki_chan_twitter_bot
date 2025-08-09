from collections import deque
from dotenv import load_dotenv
from requests_oauthlib import OAuth1
import requests
import random
import json
import os


"""
Randomly selects a motivational tweet from a list and posts it to X (Twitter).

Features:
- Keeps track of the last 10 tweet indices to avoid duplicates.
- Uses OAuth1 authentication for Twitter API v2.
- Reads tweet text from a local JSON file.
"""


# Load environment variables
load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://api.twitter.com/2")
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
MENTION_HANDLE = os.getenv("MENTION_HANDLE", "@ethan_leee9113")

# Authenticate with Twitter
auth = OAuth1(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Load tweets from file
with open("tweets_kawaii.json", "r", encoding="utf-8") as f:
    tweets = json.load(f)

# Load previous 10 tweet indices (or start fresh if missing)
try:
    with open("prev_10_tweets.json", "r", encoding="utf-8") as f:
        prev_10_num = deque(json.load(f), maxlen=10)
except (FileNotFoundError, json.JSONDecodeError):
    prev_10_num = deque(maxlen=10)

# Pick a random tweet index not in the last 10
total_tweets = len(tweets)
random_num = random.randrange(total_tweets)
while random_num in prev_10_num:
    random_num = random.randrange(total_tweets)

# Update history with new index
prev_10_num.append(random_num)

# Save updated history
with open("prev_10_tweets.json", "w", encoding="utf-8") as f:
    json.dump(list(prev_10_num), f, ensure_ascii=False, indent=2)

# Build tweet payload
tweet_text = tweets[random_num]['text']
payload = {"text": f"{tweet_text} {MENTION_HANDLE}"}

# Send tweet
url = BASE_URL.rstrip("/") + "/tweets"
response = requests.post(url, json=payload, auth=auth, timeout=15)

# Debug output
print("Posted tweet index:", random_num)
print("Last 10 indices:", list(prev_10_num))
print("Status:", response.status_code)
print("Response:", response.text)
