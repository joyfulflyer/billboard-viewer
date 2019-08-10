import functools
from flask import(
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort
from . flask_db import get_db
from . models.entry import Entry
from . models.song import Song
from . reader_utils import (
    convert_entry_to_dict, convert_to_spaces, convert_rows_to_dict
)
import json

bp = Blueprint('/search', __name__, url_prefix='/search')


@bp.before_request
def check_session():
    if 'authed' not in session:
        return redirect(url_for('/home.home'))


@bp.route('/', methods=("GET",))
def search():
    return render_template('search.html')


@bp.route('/search_results', methods=("GET",))
def search_results():
    songs = []
    if 'name' in request.args:
        name = request.args['name']
        name = convert_to_spaces(name)
        songs = get_songs_with_name(name)

    else:
        abort(400, "Bad request")

    return render_template('search_results.html',
                           songs=convert_entry_to_dict(songs))


@bp.route('/partialSong/<input>', methods=("GET",))
@bp.route('/partialSong')
def partial_song(input):
    if 'authed' not in session:
        return redirect(url_for('/home.home'))

    converted = convert_to_spaces(input)
    songs = get_songs_with_name(converted)
    songs = songs[:15]

    return json.dumps(convert_entry_to_dict(songs))


def get_songs_with_name(song_name):
    where_clause = "%" + song_name + "%"
    query = get_db().query(Song) \
                    .filter(Song.name.ilike(where_clause)) \
                    .group_by(Song.name, Song.artist) \
                    .order_by(Song.name) \
                    .limit(25)
    songs = query.all()
#    print(songs)
    return songs


# Does not actually get all songs, turned out to hit the db hard
@bp.route('/songnames', methods=("GET",))
def get_all_song_names():
    all_songs = get_db().query(Song) \
                        .group_by(Song.name, Song.artist) \
                        .limit(25) \
                        .all()
    r = convert_entry_to_dict(all_songs)
    return json.dumps(r)
