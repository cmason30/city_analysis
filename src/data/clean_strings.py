import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import pickle
import json

def get_sentiment(comment):
    stopwords = nltk.corpus.stopwords.words("english")
    cleaned_text = ' '.join([word for word in comment.split() if word not in stopwords])
    sia = SentimentIntensityAnalyzer()

    return sia.polarity_scores(cleaned_text)


with open("../../data/interim/test1.json", "r") as f:
    data = json.load(f)






