# coding=utf-8
from sqlalchemy import Unicode
from sqlalchemy import TypeDecorator
from sqlalchemy import Float
from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import DateTime


from sqlalchemy.ext.declarative import declarative_base
DeclarativeBase = declarative_base()


class CoerceUTF8(TypeDecorator):
    """Safely coerce Python bytestrings to Unicode
    before passing off to the database."""
    impl = Unicode
    def process_bind_param(self, value, dialect):
        if isinstance(value, str):
            value = value.decode('utf-8')
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            return value.encode('UTF-8')
        return value

def db_connect():

    return create_engine('mysql://root:Passw0rd!@localhost:3306/tsearch',
                        encoding='latin1', convert_unicode=False, echo=False)
    #return create_engine('sqlite:///tmp/tsearch.db', encoding='utf-8', convert_unicode=False, echo=False)


def create_tables(engine):
    DeclarativeBase.metadata.create_all(engine)


class SeriesGroup(DeclarativeBase):
    __tablename__ = 'SERIES_GROUP'

    id = Column('ID_SERIES_GROUP', Integer, nullable=False, primary_key=True)
    url = Column('URL', CoerceUTF8(100), nullable=False)
    title = Column('TITLE', CoerceUTF8(100), nullable=True)
    chapters = Column('CHAPTERS', Integer, nullable=False, default=0)
    update_date = Column('UPDATE_DATE', DateTime, nullable=True)
    status = Column('SERIES_GROUP_STATUS', CoerceUTF8(10), nullable=True)


class Series(DeclarativeBase):
    __tablename__ = 'SERIES'

    #idGroup = Column('ID_SERIES_GROUP', Integer, ForeignKey('SERIES_GROUP.ID_SERIES_GROUP'))
    idGroup = Column('ID_SERIES_GROUP', Integer)
    id = Column('ID_SERIES', Integer, nullable=False, primary_key=True)
    url = Column('URL', CoerceUTF8(200), nullable=False)
    title = Column('TITLE', CoerceUTF8(200), nullable=True)
    torrent = Column('URL_TORRENT', CoerceUTF8(200), nullable=True)
    update_date = Column('UPDATE_DATE', DateTime, nullable=True)
    size = Column('SIZE', Float, nullable=True)
    unit = Column('UNIT', CoerceUTF8(5), nullable=True)
    status = Column('SERIES_STATUS', CoerceUTF8(10), nullable=True)