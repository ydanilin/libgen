# coding=utf-8
import re
from dbms import DBMS


class ScreenMachine:
    def __init__(self):
        self.dbms = DBMS()
        self.booksFound = re.compile('books found')
        self.numbers = re.compile('\d+')

    def totalEntries(self, pulpa):
        output = None
        pagingTag = pulpa.find('td', text=self.booksFound)
        if pagingTag:
            text = pagingTag.text.strip()
            no = self.numbers.findall(text)
            if no:
                output = int(no[0])
        return output

    def processMasterTable(self, pulpa):
        tabela = pulpa.find('table', class_='c')
        if tabela:
            rows = tabela.findAll('tr')
            if rows:
                del rows[0]
                for row in rows:
                    container = self.dbms.requestContainer()
                    self.processRow(row, container)
                    self.dbms.dumpContainer(container)

    def processRow(self, row, container):
        tds = row.findAll('td')
        container['id'] = tds[0].text.strip()
        container['author'] = tds[1].text.strip()
        self.processTitleSection(tds[2], container)
        container['publisher'] = tds[3].text.strip()
        container['year'] = tds[4].text.strip()
        container['pages'] = tds[5].text.strip()
        container['language'] = tds[6].text.strip()
        container['size'] = tds[7].text.strip()
        container['extension'] = tds[8].text.strip()
        if len(row) > 13:
            container['link1'] = tds[9].find('a')['href']
            container['link2'] = tds[10].find('a')['href']
            container['link3'] = tds[11].find('a')['href']
            container['link4'] = tds[12].find('a')['href']

    def processTitleSection(self, td, container):
        alinks = td.findAll('a')
        for alink in alinks:
            ref = alink['href']
            if ref.find('series') > -1:
                container['series'] = alink.text.strip()
            if alink.has_attr('id'):
                greenTags = alink.findAll('font', {'color': 'green'})
                if len(greenTags) == 2:  # both edition and isbns
                    edition = greenTags[0].extract()
                    isbn = greenTags[1].extract()
                    container['edition'] = edition.text.strip()
                    container['isbn'] = isbn.text.strip()
                if len(greenTags) == 1:  # only isbns
                    gt = greenTags[0].extract()
                    txt = gt.text.strip()
                    if txt.find('ed') > -1:
                        # TODO: dodelat
                        container['edition']
                    else:
                        container['isbn'] = isbn.text.strip()
                # title itself
                container['title'] = alink.text.strip()

    def save(self, name):
        self.dbms.save(name)
