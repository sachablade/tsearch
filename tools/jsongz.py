import gzip
import json

def write(filename, data):
    with gzip.GzipFile(filename, 'w') as jsongzip:
        json_str = json.dumps(data)
        json_bytes = json_str.encode('utf-8')
        jsongzip.write(json_bytes)


def read(filename):
    pass
