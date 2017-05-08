import os
import h5py
import pandas as pd

from app_methods import *


def get_config_file():
    if not os.path.exists(C.__TMP__ + 'config.json.gz'):
        return dict


if __name__ == '__main__':
    import itertools
    data = map(''.join, itertools.product('ABCDEF', repeat=6))

    if not os.path.exists(C.__TMP__):
        os.makedirs(C.__TMP__)

    config = get_config_file()




    df = pd.DataFrame(data,columns=['url'])
