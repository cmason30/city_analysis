import json

import nltk
import praw
import pickle
import os
import time
import re
import statistics as stat
from transformers import pipeline


#import pymongo

cwd_ = os.getcwd()

#connString = os.environ['MONGODB_CONNSTRING']
#client = pymongo.MongoClient('localhost', 27017)

# mydb = client['citytest1'] # Set up
# posts = mydb.posts


def load_files():
    with open(f'scraperfiles/reddit_access.json', 'r') as f:
        creds = json.load(f)

    with open(f'scraperfiles/city_subreddits.json', 'r') as f:
        cities_json = json.load(f)

    return creds, cities_json


def extract_comments():

    creds, cities_json = load_files()

    reddit = praw.Reddit(
        client_id=creds['Creds']['client_id'],
        client_secret=creds['Creds']['client_secret'],
        password=creds['Creds']['password'],
        user_agent="testscript_",
        username=creds['Creds']['account'],
    )

    cities_list = cities_json['City List']
    cities_str = '+'.join(cities_list)

    count_ = 0

    for city in cities_list:

        all_subs_city = []
        subreddit_ = reddit.subreddit(city)

        for submission in subreddit_.top(time_filter="day", limit=10):

            if submission.selftext == "":
                self_text = "empty"
            else:
                self_text = submission.selftext

            submission.comments.replace_more(limit=0)  # flatten tree
            comments = submission.comments.list()  # all comments

            cleaned_com = [re.sub(r'http\S+|[^\w\s]', '', com.body) for com in comments]

            submission_dict = {
                #"subreddit": city,
                "created_utc": submission.created_utc,
                "num_comments": submission.num_comments,
                "selftext": self_text,
                "title": submission.title,
                "comments": cleaned_com,
                #"lat": cities_list[city]['lat'],
                #"lon": cities_list[city]['lon']
            }

            all_subs_city.append(submission_dict)

        cities_json['City List'][city]['data'] = all_subs_city

        if count_ == 5:
            break
        count_ += 1
        break

    print(cities_json)
# with open('test1_data.pickle', 'wb') as handle:
#     pickle.dump(bulk_subs, handle, protocol=pickle.HIGHEST_PROTOCOL)

extract_comments()


#unix_t = round(time.time())


#result = posts.insert_many(bulk_subs)

#print(client.list_database_names())



