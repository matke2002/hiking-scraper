import requests
from datetime import datetime
from bs4 import BeautifulSoup
from destination_data import DestinationData

class Zeleznicar:
    def __init__(self, destination_data_list):
        URL = 'http://www.zeleznicar.org.rs/'
        headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0",
                   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"}

        while(URL != None):
            page = requests.get(URL, headers=headers)

            soup = BeautifulSoup(page.content, 'html.parser')

            results = soup.find('div', id='maincolumn')  #.find('table', {"class": "blog"}).tbody  # .find('div',{"class": "elementor-widget-container"})

            table_blog = results.find('table', {"class": "blog"})
            tables = table_blog.find_all('table')
            for table in tables:
                if(table.table != None):
                    t = table.table.find_all('td')
                    #for ta in t:
                    #    print(ta.text)

                    title = t[2].text
                    url = t[6].find('a')['href']
                    date_str = t[4].text.split('Planinarska')[0]

                    dd = DestinationData()
                    dd.klub = 'Zeleznicar'
                    dd.url = 'http://www.zeleznicar.org.rs' + url
                    dd.title = title
                    dd.date_str = date_str
                    # dd.desc = desc_elem

                    dd.date_start, dd.date_end = self._convert_date(date_str)
                    if (dd.date_start > datetime.today()):
                        destination_data_list.append(dd)

            next = table_blog.find('a', {"class": "pagenav", "title": "Sledeća"})
            try:
                URL = 'http://www.zeleznicar.org.rs' + next['href']
            except:
                URL = None



                #print(t[2])
            #print(table.table)
            #print('----------------')

        #tr_tags = results.find_all('tr')
        #divs = tr_tags[0].find_all('div')
        #for div in divs:
        #    print(div)

        # results = soup.find('div', id='content') #.find('div',{"class": "elementor-widget-wrap"})
        #job_elems = results.find_all('div', {"class": "elementor-text-editor elementor-clearfix"}) # ('section')
        # del job_elems[0]

    def _convert_date(self, date_str):
        # print(date_str)
        date_start = None
        date_end = None
        d_split = date_str.split('-')
        godina = 0
        mesec1 = 0
        mesec2 = 0
        dan1 = 0
        dan2 = 0
        if(len(d_split)==2):
            d2=d_split[1].split('.')
            d1=d_split[0][:-1].split('.')
            dan2 = int(d2[0])
            mesec2 = int(d2[1])
            godina = int(d2[2])
            if(godina<2000):
                godina = godina + 2000
            dan1 = int(d1[0])
            try:
                mesec1 = int(d1[1])
            except:
                mesec1 = mesec2
            date_start = datetime(year=int(godina), month=int(mesec1), day=int(dan1))
            date_end = datetime(year=int(godina), month=int(mesec2), day=int(dan2))
        else:
            d1 = d_split[0].split('.')
            dan1 = int(d1[0])
            mesec1 = int(d1[1])
            godina = int(d1[2])
            date_start = datetime(year=int(godina), month=int(mesec1), day=int(dan1))
            date_end = date_start

        return date_start, date_end
