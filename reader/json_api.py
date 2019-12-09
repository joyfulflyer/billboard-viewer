import json
from flask import (Blueprint, request, jsonify)
from .find_song import get_songs_with_name
from .reader_utils import (convert_entry_to_dict, convert_to_spaces,
                           convert_rows_to_dict)
from .models.entry import Entry
from .models.chart import Chart
from .models.song import Song
from werkzeug.exceptions import abort
from .flask_db import get_db
import logging

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


def _add_entries_to_chart(chart):
    chart_entries = _get_chart_entries(chart['chartId'])
    chart_entries_mapped = map(
        lambda entry: {
            "name": entry.name,
            "artist": entry.artist,
            "place": entry.place,
            "songId": entry.song_id
        }, chart_entries)
    chart['entries'] = list(chart_entries_mapped)
    return chart


@bp.route('/chart/<int:selected_id>')
@bp.route('/chart', methods=("POST", ))
def get_songs_for_chart(selected_id):
    if selected_id is None and request.is_json:
        selected_id = request.json.id
    chart_entries = _get_chart_entries(selected_id)
    converted = list(
        map(
            lambda entry: {
                "name": entry.name,
                "artist": entry.artist,
                "place": entry.place,
                "songId": entry.song_id
            }, chart_entries))
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
    song = get_db().query(Song) \
        .filter_by(id=id) \
        .one()
    if song is None:
        abort(404, "Song not found")
    return song


def _get_entries_from_song(song):
    entries = get_db().query(Entry) \
        .filter_by(song_id=song.id).all()
    return entries


def _get_sorted_charts(song):
    entries = _get_entries_from_song(song)
    charts = list(map(_convert_entry_to_chart, entries))
    charts.sort(key=lambda chart: (chart["chartName"], chart["date"]))
    return charts
