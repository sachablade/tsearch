import unittest
from app_methods import *


class TestGetLinks(unittest.TestCase):

    def test_get_links(self):
        links=get_links_page('http://www.newpct1.com/series/')
        self.assertGreater(len(links),100,'get_links_page series devuelve %s'%(str(len(links))))

    def test_get_linkshd(self):
        links=get_links_page('http://www.newpct1.com/series-hd/')
        self.assertGreater(len(links),100,'get_links_page series-hd devuelve %s'%(str(len(links))))

    def test_get_linksvo(self):
        links=get_links_page('http://www.newpct1.com/series-vo/')
        self.assertGreater(len(links),100,'get_links_page series-vo devuelve %s'%(str(len(links))))

    def test_get_links_all(self):
        links=get_link_all()
        self.assertGreater(len(links),1000,'get_links_all devuelve %s'%(str(len(links))))



if __name__ == '__main__':
    unittest.main()