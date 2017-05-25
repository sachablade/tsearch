from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

Base = declarative_base()


class Config(Base):
    __tablename__ = 'config'
    CO_ACTION = Column(String(20), nullable=True)
    DS_VALOR = Column(String(250), nullable=True)

@contextmanager
def db_session():
    """ Creates a context with an open SQLAlchemy session.
    """
    engine = create_engine('sqlite:///tmp/tsearch.db')
    Base.metadata.create_all(engine)
    connection = engine.connect()
    db_session = scoped_session(sessionmaker(autocommit=False, autoflush=True, bind=engine))
    yield db_session
    db_session.close()
    connection.close()


