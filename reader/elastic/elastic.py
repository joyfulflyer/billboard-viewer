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


# data = {"query": {"match": {"name": {"query": query}}}}


def search_for_song(query):
    data = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["name", "artist"]
            }
        }
    }
    return submit_search(data)


def results_for_song_search(query):
    return results(search_for_song(query))


def search_name_artist(name, artist):
    data = {
        "query": {
            "bool": {
                "should": [{
                    "match": {
                        "name": {
                            "query": name
                        }
                    }
                }, {
                    "match": {
                        "artist": {
                            "query": artist
                        }
                    }
                }]
            }
        }
    }
    return submit_search(data)


def results(response):
    hits = response['hits']
    return hits['hits']


def submit_search(data):
    return s.post(create_url() + SEARCH_PATH, json=data).json()