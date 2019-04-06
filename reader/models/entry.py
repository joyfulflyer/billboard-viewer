from . base import Base
from sqlalchemy import Integer, Column, String, ForeignKey


class Entry(Base):
    __tablename__ = 'entries'

    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    artist = Column(String(128), nullable=False)
    place = Column(Integer, nullable=False)
    peak_position = Column(Integer, nullable=True)
    last_position = Column(Integer, nullable=True)
    weeks_on_chart = Column(Integer, nullable=True)
    chart_id = Column(Integer, ForeignKey("charts.id"), nullable=False)
    song_id = Column(Integer, ForeignKey("songs.id"), nullable=True)

    def __repr__(self):
        return "Entry: <id='%r', name='%r', artist='%r'>" % \
            (self.id, self.name, self.artist)
