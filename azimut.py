import requests
from bs4 import BeautifulSoup
from destination_data import DestinationData
from datetime import date, datetime

class Azimut:
    def __init__(self, destination_data_list):
        URL = 'http://www.pdazimut.rs/ostale%20stranice/najave.html'
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        current_year = str(date.today().year) + '.'
        # print('Godina je', current_year)

        results = soup.find('table')
        job_elems = results.find_all('tr')
        for job_elem in job_elems:
            # print(job_elem)
            link_elem = job_elem.find('a')
            url = 'http://www.pdazimut.rs/ostale%20stranice/' + link_elem['href']
            info = job_elem.text
            splt = info.split(current_year)
            date_str = splt[0]

            # print(info)

            dd = DestinationData()
            dd.klub = 'Azimut'
            dd.url = url
            dd.title = splt[1].replace('\n','')
            dd.date_start, dd.date_end = self._convert_date(date_str.strip())

            if (dd.date_start > datetime.today()):
                destination_data_list.append(dd)

    def _convert_date(self, date_str):
        meseci = ['januar', 'februar', 'mart', 'april', 'maj', 'jun', 'jul',
                  'avgust', 'septembar', 'oktobar', 'novembar', 'decembar']
        #print(date_str)
        dani_split = date_str.split('-')
        date1 = dani_split[0].split('.')
        date2 = date1
        date_start = datetime(year=2020, month=int(date1[1]), day=int(date1[0]))
        date_end = date_start
        if(len(dani_split) == 2):
            date2 = dani_split[1].split('.')
            date_end = datetime(year=2020, month=int(date2[1]), day=int(date2[0]))
        return date_start, date_end


