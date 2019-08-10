import json
from flask import(
    Blueprint, request
)
from . find_song import get_songs_with_name
from . reader_utils import (
    convert_entry_to_dict, convert_to_spaces, convert_rows_to_dict
)
from . models.entry import Entry
from . models.chart import Chart
from . models.song import Song
from werkzeug.exceptions import abort
from . flask_db import get_db
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.NOTSET)

bp = Blueprint('/api', __name__, url_prefix='/api')


@bp.route('/songName', methods=("POST",))
def song_from_name():
    input = request.json
    converted = convert_to_spaces(input)
    songs = get_songs_with_name(converted)
    songs = songs[:15]

    return json.dumps(convert_entry_to_dict(songs))


@bp.route('/song/<int:selected_id>')
@bp.route('/song', methods=("POST",))
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
    song = get_db().query(Song) \
        .filter_by(id=selected_id) \
        .one()
    if song is None:
        abort(404, "Song not found")
    entries = get_db().query(Entry) \
        .filter_by(song_id=song.id).all()
    charts = list(map(convert_entry_to_chart, entries))
    songDict = {
        "name": song.name,
        "artist": song.artist,
        "id": song.id,
        "charts": charts
    }
    return json.dumps(songDict)


def convert_entry_to_chart(entry):
    returnChart = {
        "place": entry.place,
        "chartId": entry.chart_id
    }
    chart = get_db().query(Chart) \
        .filter_by(id=entry.chart_id).one()
    if chart is None:
        abort(404, "No Charts")
    returnChart["chartName"] = chart.chart_type
    returnChart["date"] = chart.date_string
    return returnChart
