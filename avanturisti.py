from icalendar import Calendar
import requests
from datetime import datetime
import pytz
from destination_data import  DestinationData

class Avanturisti:
    def __init__(self, destination_data_list):
        URL = 'http://planinariavanturisti.org.rs/predstojeci-dogadjaji/month/?ical=1&tribe_display=month'
        URL = 'http://planinariavanturisti.org.rs/predstojeci-dogadjaji/month/?ical=1&tribe_display=month'
        page = requests.get(URL)

        gcal = Calendar.from_ical(page.content)
        for component in gcal.walk():
            if component.name == "VEVENT":
                #print(component.get('summary'))
                #print(component.get('dtstart').dt)
                #print(component.get('dtend').dt)
                #print(component.get('dtstamp').dt)
                #print(component.get('url'))

                dd = DestinationData()
                dd.url = component.get('url')
                dd.klub = 'Avanturisti'
                dd.title = component.get('summary')
                # dd.desc = component.get('description')
                dd.date_str = component.get('dtstart').dt
                dd.date_start = component.get('dtstart').dt
                dd.date_end = component.get('dtend').dt
                datetime_now = datetime.utcnow().replace(tzinfo=pytz.utc)
                if (dd.date_start > datetime_now):
                    destination_data_list.append(dd)


