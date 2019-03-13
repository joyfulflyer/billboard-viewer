from . base import Base
from sqlalchemy import Integer, Column, String


class Entry(Base):
    __tablename__ = 'entries'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    artist = Column(String, nullable=False)
    place = Column(Integer, nullable=False)
    peak_position = Column(Integer, nullable=True)
    last_position = Column(Integer, nullable=True)
    weeks_on_chart = Column(Integer, nullable=True)
    chart_id = Column(Integer, nullable=False)

    def __repr__(self):
        return "Entry: <id='%r', name='%r', artist='%r'>" % (self.id, self.name, self.artist)
