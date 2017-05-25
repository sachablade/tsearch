# coding=utf-8
import os
import pandas as pd

from tools.jsongz import *
from tools.dates import *
from app_methods import *
from tools.engine import *

'''
def get_config_file():
    config = {}
    if not os.path.exists(C.__TMP__):
        os.makedirs(C.__TMP__)

    if not os.path.exists(C.__TMP__ + 'config.json.gz'):
        config['full_update'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        config['tsearch'] = None
        return config
    else:
        return read(C.__TMP__ + 'config.json.gz')
'''

def get_config_file():
    with db_session() as db:
        config = db.query(Config).all()
        if len(config)==0:
            conf=Config(CO_ACTION='FULL_UPDATE',DS_VALOR=datetime.now())
            db.add(conf)
            db.flush()
        else:
            for conf in config:
                print conf.CO_ACTION



if __name__ == '__main__':
    config = get_config_file()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    d = days_between(config['full_update'], now, "%Y-%m-%d %H:%M:%S")

    if config['tsearch'] is None or d > 0:
        data = get_link_all()
        df = pd.DataFrame(data, columns=['url'])
        df['hash'] = df['url'].apply(lambda x: x.__hash__())
        df['update'] = datetime.now()
        df['chapters'] = 0
        config['tsearch'] = df.to_dict(orient='split')
        # write(C.__TMP__ + 'config.json.gz', config)

    extract = pd.DataFrame(data=config['tsearch']['data']
                           ,columns=config['tsearch']['columns'])
    extract['update'] = pd.to_datetime(extract['update'])

    mask = (extract['update'] > (datetime.now() - timedelta(7))) \
           & (extract['update'] <=datetime.now())
    df = extract.loc[mask]

    for index, row in df.iterrows():
        get_info_serie(row['url'],row['chapters'])


    # write(C.__TMP__ + 'config.json.gz', config)
