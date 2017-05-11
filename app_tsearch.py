# coding=utf-8
import os

import pandas as pd

from tools.jsongz import *
from tools.dates import *
from app_methods import *


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


if __name__ == '__main__':
    config = get_config_file()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    d = days_between(config['full_update'], now, "%Y-%m-%d %H:%M:%S")

    if config['tsearch'] is None or d >= 0:
        data = get_link_all()
        df = pd.DataFrame(data, columns=['url'])
        df['hash'] = df['url'].apply(lambda x: x.__hash__())
        config['tsearch'] = df.to_dict(orient='split')
        write(C.__TMP__ + 'config.json.gz', config)

