import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

def get_sentiment(comment):
    stopwords = nltk.corpus.stopwords.words("english")
    cleaned_text = ' '.join([word for word in comment.split() if word not in stopwords])
    sia = SentimentIntensityAnalyzer()


