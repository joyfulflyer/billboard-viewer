import unittest
from flask_testing import TestCase
from unittest.mock import MagicMock, patch
from .flask_db import get_db
from flask import Flask
from reader import create_app

from . import json_api


class TestSongById(TestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    TESTING = True

    def create_app(self):
        app = create_app(self)
        return app

    def test_get_song(self):
        response = self.client.get('/song/123')
        assert response is not None

    def tets_returns_a_song_from_db(self):
        with patch('flask_db.get_db') as get_db_mock:
            song = json_api.song_by_id_with_sub_chart_entries(1)
            assert song is not None