from flask import ( Blueprint, flash, g, redirect, render_template, request, url_for, session)
from werkzeug.exceptions import abort
from . models.entry import Entry
from . models.chart import Chart
from . flask_db import get_db
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.NOTSET)

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
    logger.error("Entry: " + repr(entry))
    if entry is None:
        abort(404, "Not found")
    n = entry.name
    a = entry.artist
    print("name: %s artist: %s" % (n, a))
    q = get_db().query(Entry.name,
                           Entry.artist,
                           Entry.place,
                           Chart.date_string,
                           Chart.type) \
                    .join(Chart) \
                    .filter(Entry.name==entry.name, Entry.artist==entry.artist)
    print(q)
    songs = q.all()
    logger.info("Songs: %r" % (songs,))
    print('Songs: %r' % (songs,))
#
#    execute('''
#                             SELECT
#                             name, artist, place, date_string, type
#                             FROM
#                             entries
#                             INNER JOIN charts ON charts.id = entries.chart_id
#                             WHERE name = ? AND artist = ?''',
#                             (entry["name"], entry["artist"])).fetchall()

    return render_template('song.html', song=entry, songs=songs)
