import requests
from datetime import datetime
from bs4 import BeautifulSoup
from destination_data import  DestinationData

class PkRadnicki:
    def __init__(self, destination_data_list):
        URL = 'https://www.pk-radnicki.rs/plan-akcija/'
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')

        results = soup.find(id='tribe-events-content')
        # print(results.prettify())

        job_elems = results.find_all('div', class_='type-tribe_events')
        for job_elem in job_elems:
            price_elem = job_elem.find('div', class_='tribe-events-event-cost')
            place_elem = job_elem.find('div', class_='tribe-events-venue-details')
            country_elem = job_elem.find('span', class_='tribe-country-name')
            link_elem = job_elem.find('a', class_='url')
            url = link_elem['href']
            title = link_elem.text.strip()
            desc_elem = job_elem.find('div', class_='description').find('p')
            date_start_str = job_elem.find('span', class_='tribe-event-date-start').text

            """            
            print(price_elem.text.strip())
            print(country_elem.text.strip())
            print(place_elem.text.replace(country_elem.text.strip(), '').strip())
            print(title, url)
            print(desc_elem.text)
            print(date_start_str)
            """
            dd = DestinationData()
            dd.url = url
            dd.klub = 'PK Radnicki'
            dd.title = title
            dd.date_start, dd.date_end = self._convert_date(date_start_str)
            dd.date_str = date_start_str
            try:
                dd.country = country_elem.text.strip()
                dd.location = place_elem.text.replace(country_elem.text.strip(), '').strip()
                dd.price = place_elem.text.replace(country_elem.text.strip(), '').strip()
            except:
                dd.country = 'SRB'
                dd.location = 'SRB'
                dd.price = '0 din'

            if (dd.date_start > datetime.now()):
                destination_data_list.append(dd)

            # print('==========================')

    def _convert_date(self, date_str):
        meseci = ['јануара', 'фебруара', 'марта', 'априла', 'маја', 'јуна', 'јула',
                  'августа', 'септембра', 'октобра', 'новембра', 'децембра']
        godina1 = 0
        godina2 = 0
        mesec1 = 0
        mesec2 = 0
        dan1 = 0
        dan2 = 0
        dani_niz = date_str.split('до')
        res1 = [elem for elem in meseci if (elem in dani_niz[0])]
        try:
            mesec1 = meseci.index(res1[0]) + 1
            dani_niz[0] = dani_niz[0].replace(res1[0], str(mesec1) + '.').strip()
        except:
            pass
        res2 = res1
        mesec2 = mesec1

        form_date = dani_niz[0].split('.')

        date_start = datetime(year=int(form_date[2]), month=int(form_date[1]), day=int(form_date[0]))
        date_end = date_start

        if(len(dani_niz)==2):
            res2 = [elem for elem in meseci if (elem in dani_niz[1])]
            try:
                mesec2 = meseci.index(res2[0]) + 1
                dani_niz[1] = dani_niz[1].replace(res2[0], str(mesec2) + '.').strip()
            except:
                pass

            form_date = dani_niz[1].split('.')
            date_end = datetime(year=int(form_date[2]), month=int(form_date[1]), day=int(form_date[0]))

        return date_start, date_end


