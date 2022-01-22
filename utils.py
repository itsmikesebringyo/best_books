import os
from pathlib import Path
from dotenv import load_dotenv


def load_env():
    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path)


def generate_header(bearer_token):
    header = {f'"Authorization": "Bearer {bearer_token}"'}


