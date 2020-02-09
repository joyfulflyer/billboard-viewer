from .elastic import elastic
from . import elastic_converter
from flask import current_app, has_app_context
import logging

logger = logging.getLogger(__name__)


def get_songs_with_name(song_name):
    verify_search_host_with_env()
    results = elastic.results_for_song_search(song_name)
    return elastic_converter.convert_elastic_results_to_songs(results)


def verify_search_host_with_env():
    if elastic.host != current_app.config['SEARCH_HOST']:
        host = current_app.config['SEARCH_HOST']
        logger.debug("setting elastic host to " + host)
        elastic.host = host
