from flask import (Blueprint, flash, g, redirect, render_template, request, url_for, session)
from sqlalchemy.orm import aliased
from werkzeug.exceptions import abort
from . models.entry import Entry
from . models.chart import Chart
from . flask_db import get_db
import logging
import json

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
#    print("name: %s artist: %s" % (n, a))
    songs_alias = aliased(Entry)
    chart_topper_alias = aliased(Entry)
    q = get_db().query(songs_alias.name, songs_alias.artist, songs_alias.place, Chart.type, Chart.date_string) \
                    .filter(songs_alias.name==entry.name, songs_alias.artist==entry.artist) \
                    .join(Chart, songs_alias.chart_id == Chart.id)
 #                   .join(chart_topper_alias, Chart.id==chart_topper_alias.chart_id) Need the data sub-queried or to group it

#    print("Initial query :" + str(q) + "\n\n")
    songs = q.all()
#    print("Second: " + str(q.subquery(Entry).join(Chart)))
#    logger.info("Songs: %r" % (songs,))
#    print('Songs: %r' % (songs,))

 #   query(Entry.name, Entry.place).

    """ entry.name, entry.artist, entry.place from entries inner join charts on chart id = entries.chart_id """
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


@bp.route('/date/<string:date_to_query>')
def songs_by_date(date_to_query):
    print(date_to_query)
    songs = get_db().query(Entry).join(Chart).filter(Chart.date_string == date_to_query).order_by(Entry.place).all()
    return json.dumps([{'name':e.name, 'artist':e.artist, 'place':e.place, 'id':e.id} for e in songs])
