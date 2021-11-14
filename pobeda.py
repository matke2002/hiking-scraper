import requests
from datetime import datetime
from bs4 import BeautifulSoup
from destination_data import  DestinationData

class Pobeda:
    def __init__(self, destination_data_list):

        URLs = [
            'https://www.pdpobeda.rs/_Foliage/showFile.php?fn=pdp_pages/najave2.php&NajavaType1=2&NajavaType2=1',
            'https://www.pdpobeda.rs/_Foliage/showFile.php?fn=pdp_pages/najave2.php&NajavaType1=2&NajavaType2=2',
            #'https://www.pdpobeda.rs/_Foliage/showFile.php?fn=pdp_pages/najave2.php&NajavaType1=2&NajavaType2=3',
            'https://www.pdpobeda.rs/_Foliage/showFile.php?fn=pdp_pages/najave2.php&NajavaType1=2&NajavaType2=4'
            # 'https://www.pdpobeda.rs/_Foliage/showFile.php?fn=pdp_pages/najave2.php&NajavaType1=2&NajavaType2=5'
        ]
        # URL = 'https://www.pdpobeda.rs/_Foliage/showFile.php?fn=pdp_pages/najave2.php&NajavaType1=2&NajavaType2=1'

        headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0",
                   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"}
        for URL in URLs:
            #print(URL)
            page = requests.get(URL, headers=headers)

            soup = BeautifulSoup(page.content, 'html.parser')
            # print(soup)

            results = soup.find('div', {"class": "big"})
            parent = results.parent
            table = parent.find('table')
            # print(table)
            job_elems = table.find_all('tr')
            for job_elem in job_elems:
                #print(job_elem)
                #print(job_elem.td.a.text)
                url = job_elem.td.a['href']
                elems = job_elem.td.a.text.split('-')
                title = '' # [e  for i in range(0, len(elems)-1)  e = e + elems[i] ]  '' # elems[0].strip()
                date_str = ''
                if(URL.endswith('1')):
                    for i in range(0, len(elems)-1):
                        title = title + elems[i]
                    date_str = elems[len(elems)-1].strip()
                else:
                    for i in range(0, len(elems)-2):
                        title = title + elems[i]
                    date_str = elems[len(elems)-2].strip() + '-' + elems[len(elems)-1].strip()
                #print(title)
                #print(date_str)
                self._convert_date(date_str)
                dd = DestinationData()
                dd.klub = 'Pobeda'
                dd.url = 'https://www.pdpobeda.rs' + url
                dd.title = title
                # dd.desc = desc_elem
                dd.date_start, dd.date_end = self._convert_date(date_str)

                destination_data_list.append(dd)
                #print('..........')
            #print('==============')

                # self._convert_date1(date_str)
    def _convert_date(self, date_str):
        meseci = ['januar', 'februar', 'mart', 'april', 'maj', 'jun', 'jul',
                  'avgust', 'septembar', 'oktobar', 'novembar', 'decembar']
        # print(date_str)
        date_start = None
        date_end = None
        godina = 0
        mesec1 = 0
        mesec2 = 0
        dan1 = 0
        dan2 = 0
        # print('godina: ', str(godina))
        dani = date_str.replace('.', '')
        dani_split = dani.split('-')
        if (len(dani_split) == 2):
            # print(dani_split[0], ' iiii... ', dani_split[1])
            res1 = [elem for elem in meseci if (elem in dani_split[0])]
            res2 = [elem for elem in meseci if (elem in dani_split[1])]
            mesec2 = meseci.index(res2[0]) + 1
            #if(len(res1) == 0):
            #    mesec1 = meseci.index(res2[0]) + 1
            #else:
            #    mesec1 = meseci.index(res1[0]) + 1
            d2_split = dani_split[1].split(' ')
            d1_split = dani_split[0].split(' ')
            dan2 = int(d2_split[0])
            dan1 = int(d1_split[0])
            godina = int(d2_split[2])
            if (bool(res1)):
                mesec1 = meseci.index(res1[0]) + 1
                # dani_split[0] = dani_split[0].replace(res1[0], '')
            else:
                mesec1 = mesec2
        else:
            # print(dani)
            res = [elem for elem in meseci if (elem in dani)]
            mesec1 = meseci.index(res[0]) + 1
            mesec2 = mesec1
            d1_split = dani.split(' ')
            dani = dani.replace(res[0], '')
            dan1 = int(d1_split[0])
            dan2 = dan1
            godina = int(d1_split[2])

        date_start = datetime(year=godina, month=mesec1, day=dan1)
        date_end = datetime(year=godina, month=mesec2, day=dan2)

        # print(date_start, ' - ', date_end)

        return date_start, date_end

