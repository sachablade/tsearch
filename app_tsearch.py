# coding=utf-8
import numpy

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
        lastupdate = datetime.now()

    if abs((datetime.now() - lastupdate).days) > 1 or res.update_date is None:
        for link in get_link_all():
            hash = link.__hash__() % (10 ** 8)
            item = session.query(SeriesGroup).filter_by(id=hash).first()
            if item is None:
               session.merge(SeriesGroup(id=hash,
                                          url=link,
                                          update_date=datetime.now()))
        session.commit()

    timeit = numpy.random.choice([10,100,300,600,3000], p=[0.5, 0.24, 0.15, 0.1, 0.01])
    print 'Ejecutando desde hace %d días' % timeit
    filter=session.query(SeriesGroup).filter(SeriesGroup.update_date >= datetime.now()-timedelta(timeit))

    for p in filter:
        try:
            get_info_serie(session, p)
            session.commit()
        except:
            print p.url
            session.rollback()

    session.close()
