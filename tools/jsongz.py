import gzip
import json

import collections


def write(filename, data):
    with gzip.GzipFile(filename, 'w') as jsongzip:
        json_str = json.dumps(data,jsongzip, ensure_ascii=False).encode('utf8')
        jsongzip.write(json_str)


def read(filename):
    with gzip.open(filename, "rb") as f:
        return convert(json.loads(f.read()))


def convert(data):
    if isinstance(data, basestring):
        return str(data.encode('utf8'))
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return data