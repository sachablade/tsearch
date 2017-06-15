# coding=utf-8
from app_methods import *
from tools.dates import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from sqlAlchemy.models import *
from datetime import timedelta

if __name__ == '__main__':
    engine = db_connect()
    create_tables(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    qry = session.query(func.max(SeriesGroup.update_date).label(
        "update_date"))

    res = qry.one()
    lastupdate = res.update_date
    if lastupdate is None:
        lastupdate= datetime.now()

    if abs((datetime.now() - lastupdate).days)>7 or res.update_date is None:
        for link in get_link_all():
            hash =  link.encode('utf-8').__hash__()%(10**8)
            item = session.query(SeriesGroup).filter_by(id=hash).first()
            if item is None:
                session.merge(SeriesGroup(id=hash,
                                            url=link,
                                            update_date=datetime.now()))
        session.commit()

    filter=session.query(SeriesGroup).filter(SeriesGroup.update_date >= datetime.now()-timedelta(7))

    for p in filter:
        try:
            get_info_serie(session, p)
            session.commit()
        except:
            print p
            session.rollback()
            raise

    session.close()
