from .base import Base
from sqlalchemy import Integer, Column, String, ForeignKey


class Song(Base):
    __tablename__ = 'songs'

    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    artist = Column(String(128), nullable=False)

    def __repr__(self):
        return "Song: <id=%r, name=%r, artist=%r>" % \
            (self.id, self.name, self.artist)

    def __eq__(self, other):
        if isinstance(other, Song):
            return self.id == other.id and self.name == other.name and self.artist == other.artist
        return False
