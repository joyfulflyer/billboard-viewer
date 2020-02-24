import unittest

from . import elastic_converter
from .models.song import Song


class ElasticConverterTest(unittest.TestCase):

    test_input = [{
        '_index': 'song',
        '_type': '_doc',
        '_id': '85995',
        '_score': 11.928007,
        '_source': {
            'name': ['Be My Baby'],
            'artist': ['Dick and DeeDee']
        }
    }, {
        '_index': 'song',
        '_type': '_doc',
        '_id': '89500',
        '_score': 11.928007,
        '_source': {
            'name': ['Be My Baby'],
            'artist': ['Andy Kim']
        }
    }, {
        '_index': 'song',
        '_type': '_doc',
        '_id': '89761',
        '_score': 11.928007,
        '_source': {
            'name': ['Be My Baby'],
            'artist': ['Cissy Houston']
        }
    }, {
        '_index': 'song',
        '_type': '_doc',
        '_id': '84995',
        '_score': 11.928007,
        '_source': {
            'name': ['Be My Baby'],
            'artist': ['The Ronettes']
        }
    }, {
        '_index': 'song',
        '_type': '_doc',
        '_id': '126946',
        '_score': 11.928007,
        '_source': {
            'name': ['Be My Baby'],
            'artist': ['Ronettes']
        }
    }, {
        '_index': 'song',
        '_type': '_doc',
        '_id': '137925',
        '_score': 11.928007,
        '_source': {
            'name': ['Be My Baby'],
            'artist': ['Vanessa Paradis']
        }
    }, {
        '_index': 'song',
        '_type': '_doc',
        '_id': '151275',
        '_score': 11.928007,
        '_source': {
            'name': ['Be My Baby'],
            'artist': ['Glitzzi Girlz']
        }
    }, {
        '_index': 'song',
        '_type': '_doc',
        '_id': '117420',
        '_score': 11.928007,
        '_source': {
            'name': ['Be My Baby'],
            'artist': ['Jody Miller']
        }
    }, {
        '_index': 'song',
        '_type': '_doc',
        '_id': '143183',
        '_score': 11.928007,
        '_source': {
            'name': ['Be My Baby'],
            'artist': ['Cappella']
        }
    }, {
        '_index': 'song',
        '_type': '_doc',
        '_id': '99078',
        '_score': 10.576747,
        '_source': {
            'name': ['Be My Baby Tonight'],
            'artist': ['John Michael Montgomery']
        }
    }]

    def test_conversion_with_score(self):
        expected_output = [{
            'id': '85995',
            'score': 11.928007,
            'name': ['Be My Baby'],
            'artist': ['Dick and DeeDee']
        }, {
            'id': '89500',
            'score': 11.928007,
            'name': ['Be My Baby'],
            'artist': ['Andy Kim']
        }, {
            'id': '89761',
            'score': 11.928007,
            'name': ['Be My Baby'],
            'artist': ['Cissy Houston']
        }, {
            'id': '84995',
            'score': 11.928007,
            'name': ['Be My Baby'],
            'artist': ['The Ronettes']
        }, {
            'id': '126946',
            'score': 11.928007,
            'name': ['Be My Baby'],
            'artist': ['Ronettes']
        }, {
            'id': '137925',
            'score': 11.928007,
            'name': ['Be My Baby'],
            'artist': ['Vanessa Paradis']
        }, {
            'id': '151275',
            'score': 11.928007,
            'name': ['Be My Baby'],
            'artist': ['Glitzzi Girlz']
        }, {
            'id': '117420',
            'score': 11.928007,
            'name': ['Be My Baby'],
            'artist': ['Jody Miller']
        }, {
            'id': '143183',
            'score': 11.928007,
            'name': ['Be My Baby'],
            'artist': ['Cappella']
        }, {
            'id': '99078',
            'score': 10.576747,
            'name': ['Be My Baby Tonight'],
            'artist': ['John Michael Montgomery']
        }]
        result = elastic_converter.clean_elastic_results(self.test_input)
        self.assertListEqual(expected_output, result)

    def test_conversion_to_song(self):
        expected_output = [
            Song(id=85995, name='Be My Baby', artist='Dick and DeeDee'),
            Song(id=89500, name='Be My Baby', artist='Andy Kim'),
            Song(id=89761, name='Be My Baby', artist='Cissy Houston'),
            Song(id=84995, name='Be My Baby', artist='The Ronettes'),
            Song(id=126946, name='Be My Baby', artist='Ronettes'),
            Song(id=137925, name='Be My Baby', artist='Vanessa Paradis'),
            Song(id=151275, name='Be My Baby', artist='Glitzzi Girlz'),
            Song(id=117420, name='Be My Baby', artist='Jody Miller'),
            Song(id=143183, name='Be My Baby', artist='Cappella'),
            Song(id=99078,
                 name='Be My Baby Tonight',
                 artist='John Michael Montgomery')
        ]
        result = elastic_converter.convert_elastic_results_to_songs(
            self.test_input)
        self.assertListEqual(expected_output, result)
