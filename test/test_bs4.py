import unittest
from .. import *



class TestStringMethods(unittest.TestCase):

    def test_get_links(self):
        links=get_links_page('http://www.newpct1.com/series/')
        self.assertGreater(len(links),1000,'get_links_page devuelve %s'%(str(len(links))))

    def test_get_links_all(self):
        links=get_link_all()
        self.assertGreater(len(links),1000,'get_links_page devuelve %s'%(str(len(links))))



if __name__ == '__main__':
    unittest.main(TestStringMethods)