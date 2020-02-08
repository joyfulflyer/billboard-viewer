from elasticsearch import Elasticsearch
import logging

from elasticsearch_dsl import connections


def global_connect():
    connections.create_connection(hosts=['localhost'], timeout=20)


def connect_elasticsearch():
    _es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    return _es


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)