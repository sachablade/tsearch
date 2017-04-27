import app_constants as C
from itertools import chain
from toolz.itertoolz import  remove
import re
from urllib2 import urlopen
from bs4 import BeautifulSoup
from memory_profiler import profile

def isin(x):
    return not any(re.findall(C.__TAG_PATTERN__, x))

def goodlinks(str):
    return str.__contains__(C.__PAGINATION_PATTERN__)

def get_links_page(url, seq=[]):
    def dropurl(x):
        return x == url or x in (seq)

    soup = BeautifulSoup(urlopen(url),'html.parser')
    return list(remove(isin, remove(dropurl, [a['href'] for a in soup.find_all('a', href=True)])))


def get_link_all():
    def letter(str):
        return not str.__contains__(C.__PAGINATION_PATTERN__)

    getlinks = list(chain(get_links_page('http://www.newpct1.com/series/'),
                     get_links_page('http://www.newpct1.com/series-hd/'),
                     get_links_page('http://www.newpct1.com/series-vo/')))

    pagination = []
    pagination_aux = list(set(remove(letter, getlinks)))
    while len(pagination_aux)>0:
        pagination_aux = list(set(remove(letter, getlinks)) - set(pagination))
        getlinks += list(chain.from_iterable([get_links_page(link, pagination) for link in pagination_aux]))
        pagination += pagination_aux
    return list(remove(goodlinks,set(getlinks)))


if __name__ == '__main__':
    goodlinks=get_link_all()
    print len(goodlinks)



