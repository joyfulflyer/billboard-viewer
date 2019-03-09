import functools
from flask import(
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort
from . flask_db import get_db
import json

bp = Blueprint('/search', __name__, url_prefix='/')


@bp.route('/', methods=("GET",))
def search():
    return render_template('search.html')


@bp.route('/search_results', methods=("GET",))
def search_results():
    songs = []
    if 'name' in request.args:
        name = request.args['name']
        name = convertToSpaces(name)
        songs = get_songs_with_name(name)

    elif 'artist' in request.args:
        artist = request.args['artist']
        artist = convertToSpaces(artist)
        songs = []

    else:
        abort(400, "Bad request")

    return render_template('search_results.html', songs=convert_rows_to_dict(songs))


@bp.route('/partialSong/<input>', methods=("GET",))
@bp.route('/partialSong')
def partial_song(input):
    converted = convertToSpaces(input)
    songs = get_songs_with_name(converted)
    songs = songs[:15]

    return json.dumps(convert_rows_to_dict(songs))


def get_songs_with_name(song_name):
    whereClause = '%' + song_name + '%'
    songs = get_db().execute('''
        SELECT * FROM entries
        WHERE UPPER(name) LIKE UPPER(?)
        GROUP BY name, artist
        ORDER BY name
        ''', (whereClause,)).fetchall()
    return songs


def convert_rows_to_dict(rows):
    return [dict(r) for r in rows]


@bp.route('/songnames', methods=("GET",))
def get_all_song_names():
    all_songs = get_db().execute('''
                                 SELECT * FROM entries GROUP BY name, artist
                                 ''').fetchall()
    r = convert_rows_to_dict(all_songs)
    return json.dumps(r)


def convertToSpaces(input):
    return " ".join(input.split('_'))
