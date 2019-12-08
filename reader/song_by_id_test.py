import unittest
from flask_testing import TestCase
from unittest.mock import MagicMock, patch
from .flask_db import get_db, db
from flask import Flask
from reader import create_app
from .models.song import Song
from .models.base import Base
from .models.entry import Entry
from .models.chart import Chart

from . import json_api


class TestSongById(TestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True

    def create_app(self):
        app = create_app(self)
        return app

    def test_get_song_returns_something(self):
        response = self.client.get('/api/song/1')
        assert response is not None

    def test_get_song_status_is_200(self):
        response = self.client.get('/api/song/1')
        assert response.status_code == 200

    def test_get_song_returns_entries(self):
        get_db().add(
            Entry(id=1,
                  name="entry name",
                  place=2,
                  artist="asdf",
                  chart_id=1,
                  song_id=1))
        get_db().add(Chart(id=1))
        get_db().commit()
        response = self.client.get('/api/song/1')
        charts = response.json['charts']
        assert charts is not None
        assert len(charts) > 0

    def setUp(self):
        Base.metadata.create_all(get_db().get_bind().engine)
        get_db().add((Song(id=1, name="songName", artist="song artist")))
        get_db().commit()

    def tearDown(self):
        Base.metadata.drop_all(get_db().get_bind().engine)
