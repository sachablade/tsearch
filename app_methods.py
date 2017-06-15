# coding=utf-8
import math
import re

import datetime

import app_constants as C

from itertools import chain
from toolz.itertoolz import remove

from urllib2 import urlopen
from bs4 import BeautifulSoup
from sqlAlchemy.models import Series

from dateutil import parser
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

def get_links_pagination(url):
    soup = BeautifulSoup(urlopen(url), 'html.parser')
    pre_links = []
    for link in soup.find_all("ul", class_="buscar-list")[0].findAll('a', href=True):
        pre_links.append(link['href'].encode('utf-8'))
    return pre_links


def get_info_serie(session, sgroup):
    try:
        soup = BeautifulSoup(urlopen(sgroup.url.decode('iso-8859-1').encode('utf-8')), 'html.parser')

        capitulos = 0

        try:
            capitulos = soup.find_all("div", class_="page-box")[1].findAll('strong')[0].text
        except Exception as e:
            print 'chapters'

        if int(capitulos.split(" ")[1]) > sgroup.chapters:
            sgroup.chapters = int(capitulos.split(" ")[1])
            '''
            try:
                info['plot'] = soup.find("div", class_="sinopsis").text
            except Exception as e:
                print 'plot'
            try:
                info['plot_description'] = soup.find("div", class_="descripcion_top").text
            except Exception as e:
                print 'plot_description'
            '''

            try:
                title = soup.find_all("ul", class_="breadcrumbs")[0].findAll('a', href=True)
                sgroup.title = str(title[len(title) - 1].text.encode('utf-8')).strip().decode('utf-8')
                print sgroup.title
            except Exception as e:
                print 'title'
            '''
            try:
                for link in soup.find_all("div", class_="entry-left")[0].findAll('img'):
                    info['image'] = link['src']
            except Exception as e:
                print 'image'
            '''
            #Obtengo la paginación para buscar enlaces
            pagination = []
            try:
                for link in soup.find_all("ul", class_="pagination")[0].findAll('a', href=True):
                    pagination.append(link['href'].encode('utf-8'))
                pagination = sorted(list(set(pagination)))
            except Exception as e:
                pagination=[]

            #Busco los enlaces de la serie
            pre_links = []
            try:
                for link in soup.find_all("ul", class_="buscar-list")[0].findAll('a', href=True):
                    pre_links.append(link['href'].encode('utf-8'))

                for pag in pagination[1:]:
                    pre_links += get_links_pagination(pag)
                pre_links = list(set(pre_links))
            except Exception as e:
                pre_links = []

            sgroup.update_date=max(get_info(session, sgroup, p) for p in pre_links)
        session.merge(sgroup)
    except:
        raise


def remove_no_printable_chars(str):
    strReturn=str.replace('\xc2\xa0', '')
    strReturn=strReturn.replace('\t', ' ')
    return strReturn


def get_info(session, sgroup, url):
    try:
        serie=Series()
        serie.idGroup=sgroup.id
        serie.id=url.encode('utf-8').__hash__()%(10**8)
        serie.url = url
        soup = BeautifulSoup(urlopen(url), 'html.parser')
        # Obtenemos el título

        torrent_title = soup.find_all("div", class_="page-box")[0].find('h1').text.encode('latin1').split('/')
        if len(torrent_title) > 1:
            torrent_title = remove_no_printable_chars(
                torrent_title[1].decode('iso-8859-1').encode('utf8'))
        else:
            torrent_title = remove_no_printable_chars(
                torrent_title[0].decode('iso-8859-1').encode('utf8'))

        serie.title=torrent_title.decode('utf-8')

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

                serie.update_date = datetime.datetime(2007, 1, 1)
                if link.text.find('Fecha:') != -1:
                    try:
                        serie.update_date = datetime.datetime.strptime(link.text.split(' ')[1].encode('utf-8'), "%d-%m-%Y")
                    except Exception as e:
                        pass


        except Exception as e:
            serie.size = 0.0
            serie.unit = ''

        try:
            tab1 = soup.find("div", {"id": "tab1"})
            for link in tab1.find_all("a", href=True):
                serie.torrent = str(link['href'])
        except Exception as e:
            serie.torrent = None
        session.merge(serie)
        return serie.update_date

    except:
        print url
        return datetime.datetime(2007, 1, 1)


