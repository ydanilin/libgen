# coding=utf-8
from miner import Miner
from screening import ScreenMachine
from bs4 import BeautifulSoup


class Alimentador:
    def __init__(self):
        self.miner = Miner()
        self.screening = ScreenMachine()

    def proceed(self):
        result = 0
        print('Welcome to Libgen parser')
        tPagesIter = [1]
        for cPage in tPagesIter:
            res = self.miner.getPage(cPage)
            pulpa = BeautifulSoup(res, 'lxml')
            # determine real amount of pages block
            if cPage == tPagesIter[0]:
                if res.find('books found') == -1:
                    result = -1
                    break
                tEntries = self.screening.totalEntries(pulpa)
                lastPage = self.miner.howManyPages(tEntries)
                msg = ("For search term '{0}' we've got "
                       "{1} books on {2} pages").format(self.miner.searchWhat,
                                                        tEntries, lastPage)
                print(msg)
                if lastPage > 1:
                    tPagesIter += list(range(2, lastPage + 1))
            self.screening.processMasterTable(pulpa)
            self.screening.save(self.miner.searchWhat)
            msg = 'Did page {0} of {1}'.format(cPage, lastPage)
            print(msg)
        return result
