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

model = pipeline('sentiment-analysis', model="finiteautomata/bertweet-base-sentiment-analysis")

with open(f'scraperfiles/reddit_access.json', 'r') as f:
    creds = json.load(f)

reddit = praw.Reddit(
    client_id=creds['Creds']['client_id'],
    client_secret=creds['Creds']['client_secret'],
    password=creds['Creds']['password'],
    user_agent="testscript_",
    username=creds['Creds']['account'],
)

with open(f'scraperfiles/city_subreddits.json', 'r') as f:
    cities_json = json.load(f)

cities_list = cities_json['City List']

cities_str = '+'.join(cities_list)

bulk_subs = []

count_ = 0
for city in cities_list:
    for submission in reddit.subreddit(city).top(time_filter="day", limit=10):

        if submission.selftext == "":
            self_text = "empty"
        else:

            self_text = submission.selftext

        #comments = [i.body for i in submission.comments]
        submission.comments.replace_more(limit=0)  # flatten tree
        comments = submission.comments.list()  # all comments

        f_com = []
        for comment in comments:
            com_list = []
            comment_rem = re.sub(r'http\S+|[^\w\s]', '', comment.body)
            #omment_rem = re.sub(r'[^\w\s]', '', comment_rem)

            print(model(comment_rem), comment_rem)
            #word_tokens = word_tokenize(comment_rem)
            # for w in word_tokens:
            #     if w not in stop_words:
            #         com_list.append(w)
            # f_com.append(com_list)

        mean_l = []
        for i in f_com:
            com = " ".join(i)
            mean_l.append(sia.polarity_scores(com)['compound'])

        city_dict = {
            "subreddit": city,
            "created_utc": submission.created_utc,
            "num_comments": submission.num_comments,
            "selftext": self_text,
            "title": submission.title,
            "comments": f_com,
            "lat": cities_list[city]['lat'],
            "lon": cities_list[city]['lon']
        }

        bulk_subs.append(city_dict)
        break
    if count_ == 15:
        break
    count_ += 1
    break

with open('test1_data.pickle', 'wb') as handle:
    pickle.dump(bulk_subs, handle, protocol=pickle.HIGHEST_PROTOCOL)


#unix_t = round(time.time())


#result = posts.insert_many(bulk_subs)

#print(client.list_database_names())



