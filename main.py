import os
import json
from utils import load_env, get_sentiment, clean_tweet


CLEANING_MAP = {
    'mentions': '@[a-zA-Z0-9_]+',
    # 'query_hashtags': '#[Bb]ook[Rr]eview|#[Bb]ook[Rr]ecommendations',
    'all_hashtags': '#[A-Za-z0-9_]+',
    'links': 'http\S+'
}


def main():
    """
    Main function
    """
    load_env()
    t_token = os.getenv('TWITTER_TOKEN')
    g_key = os.getenv('GOOGLE_BOOKS_KEY')

    # TODO - hit twitter endpoint to get list of tweets of interest for a day
        # paginate through tweet responses using 'next_token'
    
    # TODO - for each tweet in our list, 
        # get sentiment score on raw text
        # remove mentions, hashtags, links from tweet
        # use NER to get entities
        # for each entity
            # remove stopwords so only keywords remain?
            # check google and amazon api's to check if entity is a book
        # if book, perform some sort of matching (fuzzy?) from google/amazon to tweet entity
        # if book, try grabbing google/amazon rating
        # final data item should look like:
            # tweet_id, original_tweet, extracted_book, sentiment_score, google_rating, amazon_rating

    

    with open('example_response.json') as f:
        response = f.read()
    sample_response = json.loads(response)
    data = sample_response.get('data')
    m_data = sample_response.get('meta')


    for tweet in data:
        raw_text = tweet.get('text')
        print(raw_text)
        clean_text = clean_tweet(raw_text, *CLEANING_MAP.values()) 
        print(clean_text)
        raw_score = get_sentiment(raw_text)
        print(raw_score)
        print('\n')



if __name__ == '__main__':
    main()