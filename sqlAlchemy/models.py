# coding=utf-8

from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime


from sqlalchemy.ext.declarative import declarative_base

DeclarativeBase = declarative_base()


def db_connect():
    return create_engine('sqlite:///tmp/tsearch.db', encoding='utf-8',
                         echo=False)


def create_tables(engine):
    DeclarativeBase.metadata.create_all(engine)


class UrlPageSearch(DeclarativeBase):
    __tablename__ = 'URL_PAGE_SEARCH'

    id = Column('ID_URL', Integer, nullable=False, primary_key=True)
    url = Column('URL', String(100), nullable=False)
    type = Column('TYPE', String(20), nullable=True)
    update_date = Column('UPDATE_DATE', DateTime, nullable=True)
