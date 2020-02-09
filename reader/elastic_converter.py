from .models.song import Song


def convert_elastic_results_to_songs(result_array):
    converted = map(_c, result_array)
    return list(converted)


def _c(result):
    return Song(id=int(result['_id']),
                name=result['_source']['name'],
                artist=result['_source']['artist'])


def clean_elastic_results(results_array):
    convertMap = map(
        lambda result: {
            'id': result['_id'],
            'score': result['_score'],
            'name': result['_source']['name'],
            'artist': result['_source']['artist']
        }, results_array)
    return list(convertMap)
