from .elastic import elastic
from . import elastic_converter
from flask import current_app, has_app_context
import logging

logger = logging.getLogger(__name__)


def ensure_host(func):
    def wrapper_ensure_host(*args, **kwargs):
        if elastic.host != current_app.config['SEARCH_HOST']:
            host = current_app.config['SEARCH_HOST']
            logger.debug("setting elastic host to " + host)
            elastic.host = host
        return func(*args, **kwargs)

    return wrapper_ensure_host


@ensure_host
def get_songs_with_name(song_name):
    results = elastic.results_for_song_search(song_name)
    return elastic_converter.convert_elastic_results_to_songs(results)


@ensure_host
def search_name_artist(name, artist):
    search = elastic.search_name_artist(name=name, artist=artist)
    results = elastic.results(search)
    return elastic_converter.convert_elastic_results_to_songs(results)
