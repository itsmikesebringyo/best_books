import os
from utils import get_yesterday_timeframe, load_env, parse_tweets, bq_insert, access_secret_version


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
    project_id = os.getenv('PROJECT_ID')
    t_token = access_secret_version(project_id=project_id, secret_id='TWITTER_TOKEN')
    g_key = os.getenv('GOOGLE_BOOKS_KEY')
    authors_table = f'{project_id}.best_books.author_mentions'

    time_start, time_end = get_yesterday_timeframe()

    twitter_request = {
        'url': 'https://api.twitter.com/2/tweets/search/recent',
        'headers': {'Authorization': f'Bearer {t_token}'},
        'params': {'query': 'lang:en (#BookReview OR #BookRecommendations)', 
                   'max_results': 100,
                   'tweet.fields': 'created_at',
                   'start_time': time_start,
                   'end_time': time_end}
    }

    tweet_data = parse_tweets(twitter_request)

    bq_insert(tweet_data, authors_table)    

    # with open('example_response.json') as f:
    #     response = f.read()
    # sample_response = json.loads(response)
    # data = sample_response.get('data')
    # m_data = sample_response.get('meta')


    # for tweet in data:
    #     raw_text = tweet.get('text')
    #     print(raw_text)
    #     clean_text = clean_tweet(raw_text, CLEANING_MAP.values()) 
    #     print(clean_text)
    #     raw_score = get_sentiment(raw_text)
    #     print(raw_score)
    #     print('\n')



if __name__ == '__main__':
    main()
