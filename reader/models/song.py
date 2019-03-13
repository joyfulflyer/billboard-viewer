from . base import Base
from sqlalchemy import Integer, Column, String


class Song(Base):
    __tablename__ = 'songs'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    artist = Column(String)

    def __repr__(self):
        return "Song: <id='%r', name='%r', artist='%r'>" % (self.id, self.name, self.artist)
