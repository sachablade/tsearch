from datetime import datetime


def days_between(d1, d2, format):
    d1 = datetime.strptime(d1, format)
    d2 = datetime.strptime(d2, format)
    return abs((d2 - d1).days)


def datetime_handler(x):
    if isinstance(x, datetime):
        return x.strftime("%Y-%m-%d %H:%M:%S")
    raise TypeError("Unknown type")


from random import randrange
from datetime import timedelta

def random_date(start, end):
    """
    This function will return a random datetime between two datetime
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)
