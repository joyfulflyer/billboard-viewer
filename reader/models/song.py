from .base import Base
from sqlalchemy import Integer, Column, String, ForeignKey


class Song(Base):
    __tablename__ = 'songs'

    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    artist = Column(String(128), nullable=False)

    def __repr__(self):
        return "Song: <id=%r, name=%r, spotify_id=%r>" % \
            (self.id, self.name, self.spotify_id)
