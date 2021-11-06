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
