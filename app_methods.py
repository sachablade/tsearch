# coding=utf-8
import math
import string
import re
import traceback
import datetime
import warnings
import app_constants as C

from itertools import chain
from toolz.itertoolz import remove

from urllib2 import urlopen
from bs4 import BeautifulSoup
from sqlAlchemy.models import Series

__NONE_DATETIME__ = datetime.datetime(2000, 1, 1)

def isin(x):
    return not any(re.findall(C.__TAG_PATTERN__, x))


def goodlinks(str):
    return str.__contains__(C.__PAGINATION_PATTERN__)


def get_links_page(url, seq=[]):
    def dropurl(x):
        return x == url or x in (seq)

    soup = BeautifulSoup(urlopen(url), 'html.parser')
    return list(remove(isin, remove(dropurl, [a['href'].encode('UTF-8') for a in
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


def get_links_pagination(url):
    soup = BeautifulSoup(urlopen(url), 'html.parser')
    pre_links = []
    for link in soup.find_all("ul", class_="buscar-list")[0].findAll('a', href=True):
        pre_links.append(link['href'].encode('utf-8'))
    return pre_links


def get_info_serie(session, sgroup):
    try:
        soup = BeautifulSoup(urlopen(sgroup.url), 'html.parser')
        capitulos = int(soup.find_all("div", class_="page-box")[1].findAll('strong')[0].text.split(" ")[1])
        if capitulos > sgroup.chapters:
            sgroup.chapters = capitulos
            if sgroup.title is None or len(sgroup.title) == 0:
                try:
                    title = soup.find_all("ul", class_="breadcrumbs")[0].findAll('a', href=True)
                    sgroup.title = str(title[len(title) - 1].text.encode('utf-8')).strip()
                except Exception as e:
                    raise

            # Obtengo la paginación para buscar enlaces
            pagination = []
            try:
                for link in soup.find_all("ul", class_="pagination")[0].findAll('a', href=True):
                    pagination.append(link['href'].encode('utf-8'))
                pagination = sorted(list(set(pagination)))
            except Exception as e:
                # No tiene paginación
                pagination = []

            # Busco los enlaces de la serie
            pre_links = []
            try:
                for link in soup.find_all("ul", class_="buscar-list")[0].findAll('a', href=True):
                    pre_links.append(link['href'].encode('utf-8'))

                pagnumber = (sgroup.chapters / 10) + (0 if sgroup.chapters%10==0 else 1)
                if len(pagination)>0:
                    pag = '/'.join(pagination[0].split("/")[:-1]) + '/%d'
                    for i in range(2, pagnumber+1):
                        pre_links += get_links_pagination(pag%i)
                pre_links = list(set(pre_links))

                if len(pre_links) < sgroup.chapters:
                    warnings.warn("%s ---> chapters:%d real :%d" % (sgroup.title, sgroup.chapters, len(pre_links)))
            except Exception as e:
                pre_links = []

            sgroup.update_date = max(get_info(session, sgroup, p) for p in pre_links)
            print '+  ', sgroup.title
        else:
            print '*  ', sgroup.title
        session.merge(sgroup)
    except:
        print traceback.print_exc()
        raise

def get_info(session, sgroup, url):
    try:
        serie = Series()
        serie.idGroup = sgroup.id
        serie.id = url.__hash__() % (10 ** 8)
        serie.url = url
        soup = BeautifulSoup(urlopen(url), 'html.parser')
        # Obtenemos el título

        try:
            torrent_title = soup.find_all("div", class_="page-box")[0].find('h1').text.encode('UTF-8').split('/')
            torrent_title = torrent_title[len(torrent_title)-1]
            serie.title = filter(lambda x: x in string.printable, torrent_title)
        except:
            serie.title = None

        # Obtenemos el tamaño y la fecha de publicación
        try:
            for link in soup.find_all("span", class_="imp"):
                if link.text.find('Size:') != -1:
                    try:
                        size = float(link.text.split(' ')[1].encode('utf-8'))
                        serie.size = 0.0 if math.isnan(size) else size
                        serie.unit = link.text.split(' ')[2].encode('utf-8')
                    except Exception as e:
                        serie.size = 0.0
                        serie.unit = ''

                if link.text.find('Fecha:') != -1:
                    try:
                        serie.update_date = datetime.datetime.strptime(link.text.split(' ')[1].encode('utf-8'),
                                                                       "%d-%m-%Y")
                    except Exception as e:
                        serie.update_date = __NONE_DATETIME__

        except Exception as e:
            serie.size = 0.0
            serie.unit = ''

        try:
            tab1 = soup.find("div", {"id": "tab1"})
            for link in tab1.find_all("a", href=True):
                serie.torrent = str(link['href'])
        except:
            serie.torrent = None

        session.merge(serie)

        if serie.update_date is None or serie.torrent is None:
            warnings.warn("%s ---> El capitulo:'%s' no existe!" % (sgroup.title, serie.url))
            return __NONE_DATETIME__
        return serie.update_date

    except KeyboardInterrupt:
        raise

    except:
        print url
        print traceback.print_exc()
        return __NONE_DATETIME__
