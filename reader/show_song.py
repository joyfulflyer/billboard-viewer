from flask import ( Blueprint, flash, g, redirect, render_template, request, url_for, session)
from werkzeug.exceptions import abort
from . models.entry import Entry
from . models.chart import Chart
from . flask_db import get_db

bp = Blueprint('/song', __name__, url_prefix='/song')


@bp.before_request
def check_session():
    if 'authed' not in session:
        return redirect(url_for('/home.home'))


@bp.route('/<int:selected_id>')
@bp.route('/')
def song_by_id(selected_id):
    entry = get_db().query(Entry) \
                    .filter_by(id=selected_id) \
                    .one()
    if entry is None:
        abort(404, "Not found")
    songs = get_db().query(Entry.name,
                           Entry.artist,
                           Entry.place,
                           Chart.date_string,
                           Chart.type) \
                    .filter_by(name=entry.name, artist=entry.artist) \
                    .join(Chart, Chart.id == Entry.id) \
                    .all()

#    execute('''
#                             SELECT
#                             name, artist, place, date_string, type
#                             FROM
#                             entries
#                             INNER JOIN charts ON charts.id = entries.chart_id
#                             WHERE name = ? AND artist = ?''',
#                             (entry["name"], entry["artist"])).fetchall()

    return render_template('song.html', song=entry, songs=songs)
