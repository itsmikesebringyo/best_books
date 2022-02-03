import re
import requests
import datetime
from pathlib import Path
from dotenv import load_dotenv
from google.cloud import bigquery
from google_auth_oauthlib import flow
import spacy
# import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer


NLP = spacy.load('en_core_web_sm')

CLEANING_MAP = {
    'mentions': '@[a-zA-Z0-9_]+',
    # 'query_hashtags': '#[Bb]ook[Rr]eview|#[Bb]ook[Rr]ecommendations',
    'all_hashtags': '#[A-Za-z0-9_]+',
    'links': 'http\S+'
}


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


def get_yesterday_timeframe():
    """
    Returns yesterday's start and end time.
    """
    today = datetime.datetime.combine(datetime.date.today(), datetime.time(0,0,0)).astimezone()
    yest = today - datetime.timedelta(days=1)
    time_start = yest.isoformat('T')
    time_end = today.isoformat('T')
    
    return time_start, time_end


def get_authors(tweet_text):
    """
    Takes tweet text as input and returns a list of people mentioned 
    """
    doc = NLP(tweet_text)

    authors = []
    for ent in doc.ents:
        if (ent.label_ == "PERSON") and (len(ent.text.split()) > 1):
            authors.append(ent.text)

    return authors


def bq_insert(tweet_data, bq_table):
    """
    Takes a list of tweet data and bigquery table as input and inserts the data into the table
    """

    appflow = flow.InstalledAppFlow.from_client_secrets_file(
        "client_secrets.json", scopes=["https://www.googleapis.com/auth/bigquery"]
    )
    credentials = appflow.run_local_server()
    bq_client = bigquery.Client(project="", credentials=credentials)
    errors = bq_client.insert_rows_json(bq_table, tweet_data)

    if errors == []:
        print('New rows have been added')
    else:
        print(f'Encountered errors while inserting rows: {errors}')


def parse_tweets(request_object, tweets_list=[]):
    """
    Takes twitter request object as input, connects to twitter endpoint, parses the response,
    and returns a list of lists of tweets of interest
    """
    # first, get the response
    response = connect_to_endpoint(**request_object)
    data = response.get('data')
    m_data = response.get('meta')

    for tweet in data:
        tweet_id = tweet.get('id')
        text = tweet.get('text')
        created_at = tweet.get('created_at')
        
        # parse through tweet logic here...
        raw_sentiment = get_sentiment(text)

        clean_text = clean_tweet(text, CLEANING_MAP.values())
        # print(clean_text)
        # for now, we'll grab author mentions
        # later, train a custom model to recognize book titles
        authors = get_authors(clean_text)

        for author in authors:
            record = {u'tweet_id': tweet_id, u'created_at': created_at, u'text': text, u'author': author}
            tweets_list.append(record)

        # TODO: once a custom NLP model is created and works for recognizing book titles, implement logic below
        # use NER to get entities
        # for each entity
            # remove stopwords so only keywords remain?
            # check google and amazon api's to check if entity is a book
        # if book, perform some sort of matching (fuzzy?) from google/amazon to tweet entity
        # if book, try grabbing google/amazon rating
        # final data item should look like:
            # tweet_id, created_at, original_tweet, extracted_book, sentiment_score, google_rating, amazon_rating
        

    # next_token = m_data.get('next_token')
    # # if next_token exists, then recursively parse tweets again
    # if next_token:
    #     request_object['params']['pagination_token'] = next_token

    #     parse_tweets(request_object, tweets_list)

    return tweets_list


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


def clean_tweet(text, reg_expr):
    """
    Takes text and regex expressions as input and returns a cleaned version of the text.
    """
    for expr in reg_expr:
        text = re.sub(expr, '', text)
    return text


# load_env()
# token = os.getenv('TWITTER_TOKEN')
# key = os.getenv('GOOGLE_BOOKS_KEY')
# headers = generate_header(token)

hashtags = ['#BookReview', '#BookRecommendations']
hashtags_str = ' OR '.join(hashtags)
# search_url = "https://api.twitter.com/2/tweets/search/recent"
query_params = {'query': f'lang:en ({hashtags_str}) tweet.fields=created_at'}
