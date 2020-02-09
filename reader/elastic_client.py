from .elastic import elastic
from . import elastic_converter


def get_songs_with_name(song_name):
    results = elastic.results_for_song_search(song_name)
    return elastic_converter.convert_elastic_results_to_songs(results)