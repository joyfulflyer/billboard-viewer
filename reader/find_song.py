import functools
import json
import logging

from flask import (Blueprint, flash, g, redirect, render_template, request,
                   session, url_for)
from werkzeug.exceptions import abort

from .flask_db import get_db
from .models.entry import Entry
from .models.song import Song
from .reader_utils import (convert_entry_to_dict, convert_rows_to_dict,
                           convert_to_spaces)

logger = logging.getLogger(__name__)

bp = Blueprint('/search', __name__, url_prefix='/search')


@bp.route('/', methods=("GET", ))
def search():
    pass


@bp.route('/search_results', methods=("GET", ))
def search_results():
    pass


@bp.route('/partialSong/<input>', methods=("GET", ))
@bp.route('/partialSong')
def partial_song(input):
    pass


def get_songs_with_name(song_name):
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