import requests
from datetime import datetime
from bs4 import BeautifulSoup
from destination_data import DestinationData

class Avala:
    def __init__(self, destination_data_list):
        URL = 'http://www.avala.club/kategorija/izleti/'
        headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0",
                   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"}

        page = requests.get(URL, headers=headers)

        soup = BeautifulSoup(page.content, 'html.parser')

        results = soup.find('div', {"class": "background-image-inner"})

        # results = soup.find('div', id='content') #.find('div',{"class": "elementor-widget-wrap"})
        job_elems = results.find_all('div', {"class": "category-post-info"}) # ('section')
        # del job_elems[0]

        for job_elem in job_elems:
            try:
                # print(job_elem)
                url = job_elem.find('a')['href']
                title = job_elem.find('h2').text
                #regex = re.compile("/^[./]*$/")
                dot_index = 0
                try:
                    dot_index = title.index('.')-2 # or title.index('/')-2   # re.search(r'\.|/]', title)
                except:
                    dot_index = title.index('/')-2
                date_start_str = title[dot_index:].strip().lower()

                dd = DestinationData()
                dd.klub = 'Avala'
                dd.url = url
                dd.title = title
                dd.date_str = date_start_str
                # dd.desc = desc_elem

                dd.date_start, dd.date_end = self._convert_date(date_start_str)
                if (dd.date_start > datetime.now()):
                    destination_data_list.append(dd)

            except Exception as e:
                print(e)
                pass

    def _convert_date(self, date_str):
        meseci = ['јан', 'феб', 'март', 'април', 'мај', 'јун', 'јул',
                  'авг', 'сеп', 'окт', 'нов', 'дец']
        # print(date_str)
        mesec1 = 0
        mesec2 = 0
        dan1 = 0
        dan2 = 0
        godina = 0

        elementi_split = date_str.split(' ')
        if (len(elementi_split)<3):
            godina = datetime.now().year
        else:
            godina = int(elementi_split[2].replace('.', ''))
        mesec = [elem for elem in meseci if (elem in date_str)]
        mesec_indx = meseci.index(mesec[0]) + 1

        mesec1 = mesec2 = mesec_indx

        dani_niz = elementi_split[0].split('/')
        if (len(dani_niz) < 2):
            dan1 = dan2 = int(dani_niz[0].replace('.', ''))
        else:
            dan1 = int(dani_niz[0])
            dan2 = int(dani_niz[1])
        date_start = datetime(year=godina, month=mesec1, day=dan1)
        date_end = datetime(year=godina, month=mesec2, day=dan2)
        return date_start, date_end
