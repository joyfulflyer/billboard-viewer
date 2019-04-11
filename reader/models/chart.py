from . base import Base
from sqlalchemy import Integer, Column, String


class Chart(Base):
    __tablename__ = 'charts'

    id = Column(Integer, primary_key=True)
    type = Column(String(128))
    date_string = Column(String(128))
    next_chart_date = Column(String(128))

    def get_year(self):
        return self.date_string.split('-')[0]

    def __repr__(self):
        return "Chart: <id=%r, type=%r, date=%r>" % (
            self.id, self.type, self.date_string)
