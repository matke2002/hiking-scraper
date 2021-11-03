import requests
from datetime import datetime
from bs4 import BeautifulSoup
from destination_data import  DestinationData

class AltiClub:
    def __init__(self, destination_data_list):
        URL = 'https://alticlub.org.rs/plan-aktivnosti-za-2021-godinu/'
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')

        results = soup.find(id='main')
        job_elems = results.find_all('h5')
        for job_elem in job_elems:
            try:
                # print(job_elem)
                date_start_str = job_elem.find('span').text.strip()
                url = ''
                link_elem = job_elem.find('a')
                if(link_elem != None):
                    url = link_elem['href']
                desc_elem = job_elem.text.replace(date_start_str, '').replace('Link', '')
                # print(date_start_str, desc_elem, url)

                dd = DestinationData()
                dd.url = url
                dd.klub = 'Alti Club'
                dd.title = desc_elem
                dd.date_str = date_start_str
                dd.date_start, dd.date_end = self._convert_date(date_start_str)

                if (dd.date_start > datetime.today()):
                    destination_data_list.append(dd)
            except Exception as e:
                # print(e)
                pass

    def _convert_date(self, date_str):
        # print(date_str)
        godina = 2021
        date_start = None
        date_end = None
        dani_niz = date_str.split('–')
        if(len(dani_niz)==1):
            form_date = dani_niz[0].split('.')
            date_start = datetime(year=godina, month=int(form_date[1]), day=int(form_date[0]))
            date_end = date_start
        else:
            dani_niz[0] = dani_niz[0].replace('. ', '')
            form_date1 = dani_niz[0].strip().split('.')
            form_date2 = dani_niz[1].strip().split('.')
            if(len(form_date1) == 1):
                form_date1.append(form_date2[1])
            date_start = datetime(year=godina, month=int(form_date1[1]), day=int(form_date1[0]))
            date_end = datetime(year=godina, month=int(form_date2[1]), day=int(form_date2[0]))


        return date_start, date_end
