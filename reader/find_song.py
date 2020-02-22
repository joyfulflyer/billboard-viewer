from flask import Blueprint, current_app, jsonify, request
from werkzeug.exceptions import abort

from . import elastic_client
from .flask_db import get_db
from .models.song import Song
from .reader_utils import convert_entry_to_dict, convert_to_spaces

bp = Blueprint('/search', __name__, url_prefix='/api/search')


@bp.route('/query', methods=("GET", ))
def search():
    name = convert_to_spaces(request.args.get("name", default=""))
    artist = convert_to_spaces(request.args.get("artist", default=""))
    current_app.logger.debug(f"name: {name} artist: {artist}")
    result = elastic_client.search_name_artist(name=name, artist=artist)
    if len(result) == 0:
        abort(404, "Not found")
    converted = convert_entry_to_dict(result)
    return jsonify(converted)


@bp.route('/search_results', methods=("GET", ))
def search_results():
    pass


@bp.route('/partialSong/<input>', methods=("GET", ))
@bp.route('/partialSong')
def partial_song(input):
    pass


def get_songs_with_name_db(song_name):
    where_clause = "%" + song_name + "%"
    query = get_db().query(Song) \
                    .filter(Song.name.ilike(where_clause)) \
                    .group_by(Song.name, Song.artist) \
                    .order_by(Song.name) \
                    .limit(25)
    songs = query.all()
    return songs


# Does not actually get all songs, turned out to hit the db hard
@bp.route('/songnames', methods=("GET", ))
def get_all_song_names():
    pass
