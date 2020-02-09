import json
import logging

from flask import Blueprint, jsonify, request
from werkzeug.exceptions import abort
from sqlalchemy.orm.exc import NoResultFound

from .elastic_client import get_songs_with_name
from .flask_db import get_db
from .models.chart import Chart
from .models.entry import Entry
from .models.song import Song
from .reader_utils import (convert_entry_to_dict, convert_rows_to_dict,
                           convert_to_spaces)

logger = logging.getLogger(__name__)
logger.setLevel(logging.NOTSET)

bp = Blueprint('/api', __name__, url_prefix='/api')


@bp.route('/songName', methods=("POST", ))
def song_from_name():
    input = request.json['input']

    songs = get_songs_with_name(input)
    songs = songs[:15]

    return json.dumps(convert_entry_to_dict(songs))


@bp.route('/song/<int:selected_id>')
@bp.route('/song', methods=("POST", ))
def song_by_id(selected_id):
    '''
General contract:
{
    id: int,
    name: string,
    artist: string,
    charts: [
        {
            place,
            date,
            chartName,
            chartId
        }
    ]
}
    '''
    if selected_id is None and request.is_json:
        selected_id = request.json.id
    song = _get_song_from_id(selected_id)
    charts = _get_sorted_charts(song)
    songDict = {
        "name": song.name,
        "artist": song.artist,
        "id": song.id,
        "charts": charts
    }
    return jsonify(songDict)


@bp.route('/song/<int:selected_id>/more')
def song_by_id_with_sub_chart_entries(selected_id):
    '''
    General contract:
    {
        id: int,
        name: string,
        artist: string,
        charts: [
            {
                place,
                date,
                chartName,
                chartId,
                entries: [
                    name,
                    artist,
                    place,
                    songId
                ]
            }
        ]
    }
    '''
    song = _get_song_from_id(selected_id)
    charts = _get_sorted_charts(song)
    chartsWithEntries = list(map(_add_entries_to_chart, charts))
    songDict = {
        "name": song.name,
        "artist": song.artist,
        "id": song.id,
        "charts": chartsWithEntries
    }
    return jsonify(songDict)


@bp.route('/chart/<int:selected_id>')
@bp.route('/chart', methods=("POST", ))
def get_songs_for_chart(selected_id):
    if selected_id is None and request.is_json:
        selected_id = request.json.id
    chart_entries = _get_chart_entries(selected_id)
    converted = [{
        "name": entry.name,
        "artist": entry.artist,
        "place": entry.place,
        "songId": entry.song_id
    } for entry in chart_entries]
    return jsonify(converted)


@bp.route('/entry/<int:entry_id>')
def get_entry_by_id(entry_id):
    db_entry = get_db().query(Entry).filter_by(id=entry_id).first()
    if db_entry is None:
        abort(404, "Not found")
    converted = {
        "name": db_entry.name,
        "artist": db_entry.artist,
        "place": db_entry.place,
        "songId": db_entry.song_id
    }
    return jsonify(converted)


def _convert_entry_to_chart(entry):
    returnChart = {"place": entry.place, "chartId": entry.chart_id}
    chart = get_db().query(Chart) \
        .filter_by(id=entry.chart_id).one()
    if chart is None:
        abort(404, "No Charts")
    returnChart["chartName"] = chart.chart_type
    returnChart["date"] = chart.date_string
    return returnChart


def _get_chart_entries(chart_id):
    chart_entries = get_db().query(Entry) \
        .filter_by(chart_id=chart_id) \
        .all()
    return chart_entries


def _get_song_from_id(id):
    try:
        song = get_db().query(Song) \
            .filter_by(id=id) \
            .one()
    except NoResultFound:
        abort(404, "Song not found")
    if song is None:
        abort(404, "Song not found")
    return song


def _add_entries_to_chart(chart):
    chart_entries = _get_chart_entries(chart['chartId'])
    asDict = [{
        "name": entry.name,
        "artist": entry.artist,
        "place": entry.place,
        "songId": entry.song_id
    } for entry in chart_entries]
    chart['entries'] = asDict
    return chart


def _get_entries_from_song(song):
    entries = get_db().query(Entry) \
        .filter_by(song_id=song.id).all()
    return entries


def _get_sorted_charts(song):
    entries = _get_entries_from_song(song)
    charts = list(map(_convert_entry_to_chart, entries))
    charts.sort(key=lambda chart: (chart["chartName"], chart["date"]))
    return charts
