from . base import Base
from sqlalchemy import Integer, Column, String


class Chart(Base):
    __tablename__ = 'charts'

    id = Column(Integer, primary_key=True)
    type = Column(String)
    date_string = Column(String, unique=True)

    def __repr__(self):
        return "Chart: <id='%r', type='%r', date='%r'>" % (self.id, self.type, self.date_string)
