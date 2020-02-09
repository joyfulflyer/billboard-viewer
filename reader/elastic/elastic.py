import requests
import json

s = requests.Session()

DEFAULT_URL = "http://localhost:9200/"
DEFAULT_HOST = "localhost"
DEFAULT_PORT = "9200"
DEFAULT_SCHEME = "http"
SEARCH_PATH = "song/_search/"

host = DEFAULT_HOST
scheme = DEFAULT_SCHEME
port = DEFAULT_PORT


def create_url():
    return f"{scheme}://{host}:{port}/"


def search_for_song(query):
    data = {"query": {"match": {"name": {"query": query}}}}
    return s.post(create_url() + SEARCH_PATH, json=data).json()


def results_for_song_search(query):
    response = search_for_song(query)
    hits = response['hits']
    return hits['hits']