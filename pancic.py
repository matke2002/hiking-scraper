from bs4 import BeautifulSoup
from destination_data import DestinationData
from icalendar import Calendar
import requests
from datetime import datetime
from dateutil import relativedelta
import pytz

class Pancic:
    def __init__(self, destination_data_list):
        now = datetime.now()
        this_month = now.strftime("%Y-%m")
        URL = 'https://www.pdpancic.rs/events/' + this_month + '/?ical=1'
        headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0",
                   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"}
        page = requests.get(URL, headers=headers)

        gcal = Calendar.from_ical(page.content)
        for component in gcal.walk():
            if component.name == "VEVENT":
                # print(component.get('summary'))
                # print(component.get('dtstart').dt)
                # print(component.get('dtend').dt)
                # print(component.get('dtstamp').dt)
                # print(component.get('url'))

                dd = DestinationData()
                dd.url = component.get('url')
                dd.klub = 'Pancic'
                dd.title = component.get('summary')
                # dd.desc = component.get('description')
                dd.date_str = component.get('dtstart').dt
                dd.date_start = component.get('dtstart').dt
                dd.date_end = component.get('dtend').dt
                datetime_now = datetime.utcnow().replace(tzinfo=pytz.utc)
                if (dd.date_start > datetime_now):
                    destination_data_list.append(dd)

        nextmonth = now + relativedelta.relativedelta(months=1)
        next_month = nextmonth.strftime("%Y-%m")
        URL = 'https://www.pdpancic.rs/events/' + next_month + '/?ical=1'
        page = requests.get(URL, headers=headers)

        gcal = Calendar.from_ical(page.content)
        for component in gcal.walk():
            if component.name == "VEVENT":
                # print(component.get('summary'))
                # print(component.get('dtstart').dt)
                # print(component.get('dtend').dt)
                # print(component.get('dtstamp').dt)
                # print(component.get('url'))

                dd = DestinationData()
                dd.url = component.get('url')
                dd.klub = 'Pancic'
                dd.title = component.get('summary')
                # dd.desc = component.get('description')
                dd.date_str = component.get('dtstart').dt
                dd.date_start = component.get('dtstart').dt
                dd.date_end = component.get('dtend').dt
                datetime_now = datetime.utcnow().replace(tzinfo=pytz.utc)
                if (dd.date_start > datetime_now):
                    destination_data_list.append(dd)


class Pancic2:
    def __init__(self, destination_data_list):
        # https://www.pdpancic.rs/events/2021-10/?ical=1
        URL = 'https://www.pdpancic.rs/doga%c4%91aji/kategorija/akcije-u-najavi/lista/'
        headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0",
                   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"}
        page = requests.get(URL, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        print(soup)

        results = soup.find('div', {"class": "tribe-events-calendar-list"})  # .find('body')

        job_elems = results.find_all('div', {"class": "tribe-events-calendar-list__event-details tribe-common-g-col"})
        indx = 0
        for job_elem in job_elems:
            print(job_elem)
            """
            
            if (indx>2 and indx%2==0):
                # print(job_elem)
                p_tags = job_elem.find_all('p')
                a_tag = job_elem.find('a')
                url = a_tag['href']


                dd = DestinationData()
                dd.url = 'http://www.pjpancic.org.rs/Najave/' + url
                dd.klub = 'Pk J. Pancic'
                dd.title = p_tags[0].text.replace('klik za PDF', '').strip()
                dd.date_str = p_tags[1].text.replace('godine', '').strip()
                #print(dd.date_str)
                dd.date_start, dd.date_end = self._convert_date(dd.date_str)
                if (dd.date_start > datetime.today()):
                    destination_data_list.append(dd)
                #print('------------')
            """
            indx = indx + 1
    def _convert_date(self, date_str):
        # print(date_str)
        date_start = None
        date_end = None
        d_split = date_str.split('-')
        # print(len(d_split))
        if (len(d_split)==2):
            d2 = d_split[1].split('.')
            date_end = datetime(year=int(d2[2]), month=int(d2[1]), day=int(d2[0]))
            d1 = d_split[0].strip().split('.')
            for i in range(len(d1)-1, 3):
                if(len(d1[i])==0):
                    d1[i] = d2[i]
                    d1.append('')
            date_start = datetime(year=int(d1[2]), month=int(d1[1]), day=int(d1[0]))
        else:
            d1 = d_split[0].split('.')
            date_start = datetime(year=int(d1[2]), month=int(d1[1]), day=int(d1[0]))
            date_end = date_start

        return date_start, date_end
