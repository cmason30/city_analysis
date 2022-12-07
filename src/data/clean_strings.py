import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import pickle

def get_sentiment(comment):
    stopwords = nltk.corpus.stopwords.words("english")
    cleaned_text = ' '.join([word for word in comment.split() if word not in stopwords])
    sia = SentimentIntensityAnalyzer()

    return sia.polarity_scores(cleaned_text)


with open('/Users/colinmason/Desktop/python-projects/city_analysis/test1_data.pickle', 'rb') as f:
    data = pickle.load(f)

print(data)



