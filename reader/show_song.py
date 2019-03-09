from flask import ( Blueprint, flash, g, redirect, render_template, request, url_for)
from werkzeug.exceptions import abort

from . flask_db import get_db

bp = Blueprint('/song', __name__, url_prefix='/song')


@bp.route('/<int:selected_id>')
@bp.route('/')
def song_by_id(selected_id):
    entry = get_db().execute('''
                     SELECT * FROM entries WHERE id = ?
                     ''', (selected_id,)).fetchone()
    if entry is None:
        abort(404, "Not found")
    songs = get_db().execute('''
                             SELECT
                             name, artist, place, date_string, type
                             FROM
                             entries
                             INNER JOIN charts ON charts.id = entries.chart_id
                             WHERE name = ? AND artist = ?''',
                             (entry["name"], entry["artist"])).fetchall()

    return render_template('song.html', song=entry, songs=songs)
