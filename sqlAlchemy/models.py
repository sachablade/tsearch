# coding=utf-8
from sqlalchemy import Float

from sqlalchemy import ForeignKey

from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime


from sqlalchemy.ext.declarative import declarative_base

DeclarativeBase = declarative_base()


def db_connect():
    #return create_engine('mysql://root:021010@localhost:3306/tsearch',
    #                     encoding='utf-8', echo=False)
    return create_engine('sqlite:///tmp/tsearch.db', encoding='utf-8', echo=False)


def create_tables(engine):
    DeclarativeBase.metadata.create_all(engine)


class SeriesGroup(DeclarativeBase):
    __tablename__ = 'SERIES_GROUP'

    id = Column('ID_SERIES_GROUP', Integer, nullable=False, primary_key=True)
    url = Column('URL', String(100), nullable=False)
    title = Column('TITLE', String(100), nullable=True)
    chapters = Column('CHAPTERS', Integer, nullable=False, default=0)
    update_date = Column('UPDATE_DATE', DateTime, nullable=True)


class Series(DeclarativeBase):
    __tablename__ = 'SERIES'

    idGroup = Column('ID_SERIES_GROUP', Integer, ForeignKey('SERIES_GROUP.ID_SERIES_GROUP'))
    id = Column('ID_SERIES', Integer, nullable=False, primary_key=True)
    url = Column('URL', String(200), nullable=False)
    title = Column('TITLE', String(200), nullable=True)
    torrent = Column('URL_TORRENT', String(200), nullable=True)
    update_date = Column('UPDATE_DATE', DateTime, nullable=True)
    size = Column('SIZE', Float, nullable=True)
    unit = Column('UNIT', String(5), nullable=True)
