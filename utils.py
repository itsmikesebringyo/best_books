import json
import os
import requests
from pathlib import Path
from dotenv import load_dotenv


def load_env():
    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path)


def bearer_auth(r):

    r.headers["Authorization"] = f"Bearer {token}"
    r.headers["User-Agent"] = "best_books"
    return r


def connect_to_endpoint(url, params):
    response = requests.get(
        url=url,
        auth=bearer_auth,
        params=params
    )
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def build_query():

    endpoint_url = 'https://api.twitter.com/2/tweets/search/all'

    query_params = {
        'query': 'book',
        'max_results': 1
    }
    return endpoint_url, json.dumps(query_params)


load_env()
token = os.getenv('TWITTER_TOKEN')

search_url = "https://api.twitter.com/2/tweets/search/recent"

query_params = {'query': '#book','max_results': 10}

json_response = connect_to_endpoint(search_url, query_params)
print(json_response)

