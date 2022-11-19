import json
import praw
import os
import pymongo

cwd_ = os.getcwd()

#connString = os.environ['MONGODB_CONNSTRING']
client = pymongo.MongoClient('localhost', 27017)

mydb = client['citytest1']
posts = mydb.posts

with open(f'{cwd_}/scraperfiles/reddit_access.json', 'r') as f:
    creds = json.load(f)

reddit = praw.Reddit(
    client_id=creds['Creds']['client_id'],
    client_secret=creds['Creds']['client_secret'],
    password=creds['Creds']['password'],
    user_agent="testscript_",
    username=creds['Creds']['account'],
)

with open(f'{cwd_}/datafiles/city_subreddits.json', 'r') as f:
    cities_json = json.load(f)

cities_list = cities_json['City List']

cities_str = '+'.join(cities_list)

bulk_subs = []

count_ = 0
for city in cities_list:
    for submission in reddit.subreddit(city).top(time_filter="day", limit=25):

        if submission.selftext == "":
            self_text = "empty"
        else:
            self_text = submission.selftext

        city_dict = {
            "subreddit": city,
            "created_utc": submission.created_utc,
            "num_comments": submission.num_comments,
            "selftext": self_text,
            "title": submission.title
        }

        bulk_subs.append(city_dict)
        break
    if count_ == 5:
        break
    count_ += 1

result = posts.insert_many(bulk_subs)

print(client.list_database_names())



