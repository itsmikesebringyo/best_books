import json
import re
import os
import requests
from pathlib import Path
from dotenv import load_dotenv
import spacy
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def load_env():
    """
    A quick way to load environment variables
    """
    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path)


def generate_header(token):
    """
    Takes bearer token as input and returns a request header
    """
    header = {}
    header["Authorization"] = f"Bearer {token}"
    return header


def connect_to_endpoint(url, headers, params):
    """
    Takes url, headers, and params as input.. hits endpoint, and returns response json
    """
    response = requests.get(
        url=url,
        headers=headers,
        params=params
    )
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def get_sentiment(tweet_text):
    """
    Takes text of tweet as input and returns a sentiment score
    """

    # future work... train custom NLP model to perform sentiment analysis
    # currently using NLTK's pretrained VADER sentiment analyzer. This analyzer is best suited
    # for short sentences with slang and abbreviations so it suits Twitter text analysis 
    sia = SentimentIntensityAnalyzer()
    score = sia.polarity_scores(tweet_text).get('compound')
    return score


def clean_tweet(tweet_text):
    """
    Takes body of tweet as input and returns a cleaned version of the tweet.
    """
    tweet_text = remove_mentions(tweet_text)
    tweet_text = remove_hashtags(tweet_text)
    return tweet_text


def remove_mentions(text):
    """
    Takes text as input and removes mentions of user
    """
    clean_text = re.sub("@[a-zA-Z0-9_]+", "", text)
    return clean_text


def remove_hashtags(text):
    """
    Takes text as input and removes hashtags used in query
    """
    hashtag_re = '#[Bb]ook[Rr]eview|#[Bb]ook[Rr]ecommendations' # TODO this is hardcoded for now, look into
    # improving this in the event that more hashtags are added
    clean_text = re.sub(hashtag_re, '', text)
    return clean_text


# load_env()
# token = os.getenv('TWITTER_TOKEN')
# key = os.getenv('GOOGLE_BOOKS_KEY')
# headers = generate_header(token)

# hashtags = ['#BookReview', '#BookRecommendations']
# hashtags_str = ' OR '.join(hashtags)
# search_url = "https://api.twitter.com/2/tweets/search/recent"
# query_params = {'query': f'lang:en ({hashtags_str})'}
