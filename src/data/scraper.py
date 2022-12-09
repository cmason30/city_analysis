import json
import praw
import pickle
import re
from dotenv import load_dotenv
from datetime import datetime
import os


def load_files(): # Gets initial City JSON file

    with open('/Users/colinmason/Desktop/python-projects/city_analysis/data/city_subreddits.json', 'r') as f:
        cities_json = json.load(f)

    return cities_json


def get_creds(): # Loads environment variables for API keys
    load_dotenv()

    return os.environ


def clean_text(text):

    return re.sub(r'http\S+|[^\w\s]', '', text)



def extract_comments():
    """Extracts comments from 54 city subreddits. Returns a nested dictionary:
    {Current Date: {City Subreddit: {lat:int, lon:int, Data:{[comment1, comment2, comment3,...'"""

    cities_json = load_files()
    creds = get_creds()

    reddit = praw.Reddit(
        client_id=creds['CLIENTID'],
        client_secret=creds["CLIENTSECRET"],
        password=creds["PASSWORD"],
        user_agent="testscript_",
        username=creds['USERNAME'],
    )

    out_dict = {}
    today_date = datetime.today().strftime('%Y-%m-%d')
    out_dict[today_date] = {}

    cities_list = cities_json['city_subreddits']
    total_cities = len(cities_list)
    cnt_ = 0

    for city in cities_list:

        out_dict[today_date][city] = {}

        cnt_ += 1
        print(f"Extracting data from subreddit: {city}... \t {cnt_}/{total_cities}")

        all_subs_city = []
        subreddit_ = reddit.subreddit(city)

        for submission in subreddit_.top(time_filter="day"):

            if submission.selftext == "":
                self_text = "empty"
            else:
                self_text = clean_text(submission.selftext)

            # submission.comments.replace_more(limit=0)  # flatten tree
            # comments = submission.comments.list()  # all comments
            #cleaned_text = [re.sub(r'http\S+|[^\w\s]', '', com.body) for com in comments]

            submission_dict = {
                "created_utc": submission.created_utc,
                "num_comments": submission.num_comments,
                "selftext": self_text,
                "title": clean_text(submission.title),
                #"comments": cleaned_com,
            }

            all_subs_city.append(submission_dict)

        out_dict[today_date][city]['lat'] = cities_list[city]['lat']
        out_dict[today_date][city]['lon'] = cities_list[city]['lon']

        out_dict[today_date][city]['submission'] = all_subs_city

    return out_dict


if __name__ == "__main__":

    city_output = extract_comments()
    with open("test_only_title.json", "w") as outfile:
        json.dump(city_output, outfile)


