import functools
from flask import(
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort
from . flask_db import get_db
from . models.entry import Entry
import json
from . find_song import bp, convertToSpaces


bp = Blueprint('/artist', __name__, url_prefix='/artist')


@bp.before_request
def check_session():
    if 'authed' not in session:
        return redirect(url_for('/home.home'))


@bp.route('/', methods=("GET",))
def search():
    return render_template('artist_search.html')


@bp.route('/partial', methods=("GET",))
def partial_artist():
    if 'artist' in request.args:
        artist = request.args['artist']
        artist = convertToSpaces(artist)
        artists = get_artists_with_name(artist)
    else:
        abort(400, "Bad request")

    return render_template('partial_artist.html', artists=[e[0] for e in artists])


def get_artists_with_name(artist_name):
    where_clause = "%" + artist_name + "%"
    query = get_db().query(Entry.artist) \
                    .filter(Entry.artist.ilike(where_clause)) \
                    .group_by(Entry.artist) \
                    .limit(25)
    return query.all()


@bp.route('/name/<input>')
def songs_from_artist(input):
    artist = get_db().query(Entry) \
                     .filter(Entry.artist == input) \
                     .order_by(Entry.place) \
                     .group_by(Entry.name) \
                     .all()
    if len(artist) is 0:
        abort(400, "Not found")


    return render_template('artist_songs.html', songs=[{'name':e.name, 'place':e.place, 'id':e.id} for e in artist])


