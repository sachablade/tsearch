# coding=utf-8
from app_methods import *
from tools.dates import *

from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

from sqlAlchemy.models import *


if __name__ == '__main__':
    engine = db_connect()
    create_tables(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    qry = session.query(func.max(UrlPageSearch.update_date).label(
        "update_date"))

    res = qry.one()
    lastupdate = res.update_date
    if lastupdate is None:
        lastupdate= datetime.now()

    if abs((datetime.now() - lastupdate).days)>7 or res.update_date is None:
        for link in get_link_all():
            hash =  link.encode('utf-8').__hash__()%(10**8)
            item = session.query(UrlPageSearch).filter_by(id=hash).first()
            if item is None:
                session.merge(UrlPageSearch(id=hash,
                                            url=link,
                                            type="newpct",
                                            update_date=datetime.now()))
        session.commit()
    session.close()
