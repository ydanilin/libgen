# coding=utf-8
from math import modf
from requests import Session


class Miner:
    def __init__(self):
        self.userAgent = \
            'Mozilla/5.0 (Windows NT 5.1; rv:45.0) Gecko/20100101 Firefox/45.0'
        self.host = 'gen.lib.rus.ec'
        self.baseUrl = 'http://' + self.host
        # http://gen.lib.rus.ec/search.php?
        # req=trading&
        # lg_topic ???
        # open=0&
        # res=100&
        # view=simple&
        # phrase=0&
        # column=def&
        # sort=def&
        # sortmode=ASC&
        # page=9
        self.searchStr = self.baseUrl + '/search.php'
        self.hitsPerPage = 100
        self.timeout = 60
        # create Session
        self.S = Session()
        self.S.headers.update({'Host': self.host})  # default headers
        self.S.headers.update({'User-Agent': self.userAgent})
        self.S.headers.update({'Referer': self.baseUrl})
        # payload
        self.searchWhat = 'trading'
        self.payload = {'req': self.searchWhat,
                        'lg_topic': 'libgen',
                        'open': 0,
                        'res': self.hitsPerPage,
                        'view': 'simple',
                        'phrase': 0,
                        'column': 'def',
                        'sort': 'def',
                        'sortmode': 'ASC',
                        'page': 1,
                        }

    def getPage(self, page):
        self.payload['page'] = page
        resp = self.S.get(self.searchStr, params=self.payload)
        return resp.content.decode('utf-8')

    def howManyPages(self, totalEntries):
        pagesTuple = modf(1.0*totalEntries/self.hitsPerPage)
        if pagesTuple[0] > 0:
            tPages = int(pagesTuple[1] + 1)
        else:
            tPages = int(pagesTuple[1])
        return tPages
