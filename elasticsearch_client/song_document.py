from elasticsearch_dsl import Document, Text


class SearchableSong(Document):
    name = Text()
    artist = Text()

    class Index:
        name = 'song'
