# coding=utf-8
import app_constants as C
from datetime import datetime
from itertools import chain
from toolz.itertoolz import remove
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

    soup = BeautifulSoup(urlopen(url), 'html.parser')
    return list(remove(isin, remove(dropurl, [a['href'] for a in
                                              soup.find_all('a', href=True)])))


def get_link_all():
    def letter(str):
        return not str.__contains__(C.__PAGINATION_PATTERN__)

    getlinks = list(chain(get_links_page('http://www.newpct1.com/series/'),
                          get_links_page('http://www.newpct1.com/series-hd/'),
                          get_links_page('http://www.newpct1.com/series-vo/')))

    pagination = []
    pagination_aux = list(set(remove(letter, getlinks)))
    while len(pagination_aux) > 0:
        pagination_aux = list(set(remove(letter, getlinks)) - set(pagination))
        getlinks += list(chain.from_iterable(
            [get_links_page(link, pagination) for link in pagination_aux]))
        pagination += pagination_aux
    return list(remove(goodlinks, set(getlinks)))


def get_info_serie(url, chapters):
    soup = BeautifulSoup(urlopen(url), 'html.parser')
    info = {'title':'','chapters': 0, 'plot': '', 'plot_description': ''}

    update_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        capitulos = soup.find_all("div", class_="page-box")[1].findAll(
            'strong')[0].text
        info['chapters'] = int(capitulos.split(" ")[1])
    except Exception as e:
        print 'chapters'

    if info['chapters'] > chapters:
        try:
            info['plot'] = soup.find("div", class_="sinopsis").text
        except Exception as e:
            print 'plot'
        try:
            info['plot_description'] = soup.find("div", class_="descripcion_top").text
        except Exception as e:
            print 'plot_description'
        try:
            title = soup.find_all("ul", class_="breadcrumbs")[0].findAll('a', href=True)
            info['title'] = str(title[len(title) - 1].text.encode('utf-8')).strip()
            print info['title']
        except Exception as e:
            print 'title'
        try:
            for link in soup.find_all("div", class_="entry-left")[0].findAll('img'):
                info['image'] = link['src']
        except Exception as e:
            print 'image'




if __name__ == '__main__':
    get_info_serie('http://www.newpct1.com/series-hd/el-pequeño-quinquin'
                   '/2018', 0)
