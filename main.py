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