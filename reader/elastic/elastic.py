import requests
import json

s = requests.Session()

DEFAULT_URL = "http://localhost:9200/"
SEARCH_PATH = "song/_search/"

_url = DEFAULT_URL


def set_url(url):
    _url = url


def search_for_song(query):
    data = {"query": {"match": {"name": {"query": query}}}}
    return s.post(DEFAULT_URL + SEARCH_PATH, json=data).json()


def results_for_song_search(query):
    response = search_for_song(query)
    hits = response['hits']
    return hits['hits']