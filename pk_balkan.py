import requests
from datetime import datetime
from bs4 import BeautifulSoup
from destination_data import  DestinationData

class PkBalkan:
    def __init__(self, destination_data_list):
        URL = 'http://pkbalkan.org/'
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')

        results = soup.find(id='content').find('div', {"class": "cat-posts-stacked"})
        job_elems = results.find_all('div', {"class": "post clearfix"})
        for job_elem in job_elems:
            #print(job_elem)
            a_tag = job_elem.find('a')
            title = job_elem.find('img')['title'].split('–')
            # 'KOZARA I PLITVICE – 12. do 14. 6. 2020.'
            url = a_tag['href']
            desc_elems = job_elem.find_all('p')
            desc_elem = ' '.join(el.text for el in desc_elems)

            dd = DestinationData()
            dd.url = url
            dd.klub = 'Pk Balkan'
            dd.desc = desc_elem
            dd.title = title[0].strip()
            dd.date_str = title[len(title)-1].strip()
            dd.date_start, dd.date_end = self._convert_date(dd.date_str)
            if (dd.date_start > datetime.now()):
                destination_data_list.append(dd)

    def _convert_date(self, date_str):
        # print(date_str)
        date_start = None
        date_end = None
        tmp_date_str = date_str.replace('i', 'do')
        d_split = tmp_date_str.split('do')
        # print(len(d_split))
        if (len(d_split) == 2):
            d2 = d_split[1].split('.')
            date_end = datetime(year=int(d2[2]), month=int(d2[1]), day=int(d2[0]))
            d1 = d_split[0].strip().split('.')
            for i in range(len(d1) - 1, 3):
                if (len(d1[i]) == 0):
                    d1[i] = d2[i]
                    d1.append('')
            date_start = datetime(year=int(d1[2]), month=int(d1[1]), day=int(d1[0]))
        else:
            d1 = d_split[0].split('.')
            date_start = datetime(year=int(d1[2]), month=int(d1[1]), day=int(d1[0]))
            date_end = date_start

        return date_start, date_end
