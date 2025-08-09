import os
import json
import random
import requests
from requests_oauthlib import OAuth1
from dotenv import load_dotenv

load_dotenv()


BASE_URL = os.getenv("BASE_URL")
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

# signs it for twitter to verify its from me
auth = OAuth1(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)


# read from the json file of all the tweets
with open("tweets_kawaii.json", "r", encoding="utf-8") as f:
    tweets = json.load(f)


# read the prev_10_tweets json file
with open("prev_10_tweets.json", 'r', encoding="utf-8") as f:
    prev_10_num = json.load(f)


# chagning endpoints to tweet
url = BASE_URL.rstrip("/") + "/tweets"


random_num = random.randint(0, 999)

# keep generating a random num until num is not in the list of prev 10
while random_num in prev_10_num:
    random_num = random.randint(0, 999)


# remove the first one and add new num at the end of the list
prev_10_num = prev_10_num[1:9]
prev_10_num.append(random_num)

with open("prev_10_tweets.json", 'w', encoding='utf-8') as f:
    json.dump(prev_10_num, f, ensure_ascii=False, indent=2)


tweet = tweets[random_num]['text']


payload = {"text": f'{tweet} @ethan_leee9113'}


# sending the post request to twitter api
r = requests.post(url, json=payload, auth=auth, timeout=15)

print(prev_10_num)
print(random_num)
print("Status:", r.status_code)
print("Body:", r.text)
