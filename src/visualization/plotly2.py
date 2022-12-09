import json
from nltk.sentiment import SentimentIntensityAnalyzer
import plotly.graph_objects as go
import pandas as pd
import os

json_pth = os.path.abspath(os.path.join(__file__ ,"../../../data/interim/test_only_title.json"))
with open(json_pth, 'r') as f:
    cities_json = json.load(f)


cities1 = cities_json['2022-12-08']
#cities2 = cities_json['Date']['2022-12-07']


#print(cities)

def extract_location(city_json):

    lat = city_json['lat']
    lon = city_json['lon']

    return lat, lon


def extract_sentiment_score_titles(city_json):

    sia = SentimentIntensityAnalyzer()

    sentiment_list = []

    for i in city_json:

       # print(i)

        if len(str(i['selftext'])) > 5:
            sentiment_list.append(sia.polarity_scores(i['selftext']))

        sentiment_list.append(sia.polarity_scores(i['title']))

    compound_scores = [d['compound'] for d in sentiment_list if 'compound' in d]

    num_posts = len(compound_scores)
    mean_sentiment = sum(compound_scores) / len(compound_scores)

    return mean_sentiment, num_posts

#
# lat, lon = extract_location(cities1['NYC'])
# sent, cnt_ = extract_sentiment_score_titles(cities1['NYC']['submission'])

def city_to_pandas(date_json):

    lat_list = []
    lon_list = []
    sent_list = []
    city_name = []
    num_post_list = []

    for key in date_json:
        city = date_json[key]
        lat_, lon_ = extract_location(city)
        mean_sentiment, num_posts = extract_sentiment_score_titles(city['submission'])

        city_name.append(key)
        lat_list.append(lat_)
        lon_list.append(lon_)
        sent_list.append(mean_sentiment)
        num_post_list.append(num_posts)


    out_vals = ({
        'subreddit': city_name,
        'lat': lat_list,
        'lon': lon_list,
        'sent': sent_list,
        'num_posts': num_post_list
    })

    return pd.DataFrame(out_vals)


def make_fig(df):
    fig = go.Figure()
    #
    fig.add_trace(go.Scattergeo(locationmode = 'USA-states',
                                lon=df['lon'],
                                lat=df['lat'],
                                text=df['subreddit'],
                                marker=dict(size=100/25,
                                            cauto=True,
                                            line_color='rgb(40,40,40)',
                                            line_width=0.5,
                                            sizemode='area'
                                            ),
                                name="Text2"))

    fig.update_layout(
            title_text='2014 US city populations<br>(Click legend to toggle traces)',
            showlegend=True,
            geo=dict(
                scope='usa',
                landcolor='rgb(217, 217, 217)',
            )
        )

    fig.show()


df = city_to_pandas(cities1)

make_fig(df)




