import json
import praw
import os

connString = os.environ['MONGODB_CONNSTRING']

with open('reddit_access.json', 'r') as f:
    creds = json.load(f)

reddit = praw.Reddit(
    client_id=creds['Creds']['client_id'],
    client_secret=creds['Creds']['client_secret'],
    password=creds['Creds']['password'],
    user_agent="testscript_",
    username=creds['Creds']['account'],
)

with open('city_subreddits.json', 'r') as f:
    cities_json = json.load(f)

cities_list = cities_json['City List']

cities_str = '+'.join(cities_list)

for city in cities_list:
    for submission in reddit.subreddit(city).top(time_filter="day", limit=25):
        print(submission.subreddit)


