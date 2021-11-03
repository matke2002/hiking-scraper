import requests
from datetime import datetime
from bs4 import BeautifulSoup
from destination_data import  DestinationData

class Kopaonik:
    def __init__(self, destination_data_list):
        URL = 'https://www.psd-kopaonik.org.rs/planinarenje/najave-akcija-pl.html'
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')

        results = soup.find(id='s5_component_wrap_inner').find('tbody')
        job_elems = results.find_all('tr')
        for job_elem in job_elems:
            try:
                # print(job_elem)
                date_start_str = job_elem.find('td',{"class": "list-date small"}).text.strip()
                url = ''
                title = ''
                link_elem = job_elem.find('a')
                if(link_elem != None):
                    url = link_elem['href']
                    title = link_elem.text.strip()
                #desc_elem = job_elem.text.replace(date_start_str, '').replace('Link', '')
                # print(date_start_str, desc_elem, url)

                dd = DestinationData()
                dd.klub = 'Kopaonik'
                dd.url = 'https://www.psd-kopaonik.org.rs/' + url
                dd.title = title
                #dd.desc = desc_elem
                dd.date_start, dd.date_end = self._convert_date(date_start_str)

                if (dd.date_start > datetime.today()):
                    destination_data_list.append(dd)
            except Exception as e:
                # print(e)
                pass
    def _convert_date(self, date_str):
        meseci = ['јануар', 'фебруар', 'март', 'април', 'мај', 'јун', 'јул',
                  'август', 'септембар', 'октобар', 'новембар', 'децембар']
        # print(date_str)

        godina1 = 0
        godina2 = 0
        mesec1 = 0
        mesec2 = 0
        dan1 = 0
        dan2 = 0
        dani_split = date_str.split(' ')
        godina1 = dani_split[2]
        dan1 = dani_split[0]
        mesec1 = meseci.index(dani_split[1]) + 1
        date_start = datetime(year=int(godina1), month=int(mesec1), day=int(dan1))
        date_end = date_start
        return date_start, date_end

