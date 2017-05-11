from datetime import datetime

def days_between(d1, d2, format):
    d1 = datetime.strptime(d1, format)
    d2 = datetime.strptime(d2, format)
    return abs((d2 - d1).days)