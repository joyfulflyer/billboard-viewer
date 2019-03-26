import functools
from flask import(
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort
from . flask_db import get_db
from . models.entry import Entry
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
        name = convertToSpaces(name)
        songs = get_songs_with_name(name)

    elif 'artist' in request.args:
        artist = request.args['artist']
        artist = convertToSpaces(artist)
        songs = []

    else:
        abort(400, "Bad request")

    return render_template('search_results.html',
                           songs=convert_entry_to_dict(songs))


@bp.route('/partialSong/<input>', methods=("GET",))
@bp.route('/partialSong')
def partial_song(input):
    if 'authed' not in session:
        return redirect(url_for('/home.home'))

    converted = convertToSpaces(input)
    songs = get_songs_with_name(converted)
    songs = songs[:15]

    return json.dumps(convert_entry_to_dict(songs))


def get_songs_with_name(song_name):
    where_clause = "%" + song_name + "%"
    query = get_db().query(Entry) \
                    .filter(Entry.name.ilike(where_clause)) \
                    .group_by(Entry.name, Entry.artist) \
                    .order_by(Entry.name) \
                    .limit(25)
    songs =  query.all()
    print(songs)
    return songs


def convert_entry_to_dict(entries):
    r= [{'name':e.name, 'artist':e.artist, 'id':e.id} for e in entries]
    return r


def convert_rows_to_dict(rows):
    return [dict(r) for r in rows]


# Does not actually get all songs, turned out to hit the db hard
@bp.route('/songnames', methods=("GET",))
def get_all_song_names():
    all_songs = get_db().query(Entry) \
                        .group_by(Entry.name, Entry.artist) \
                        .limit(25) \
                        .all()
    r = convert_entry_to_dict(all_songs)
    return json.dumps(r)


def convertToSpaces(input):
    return " ".join(input.split('_'))
