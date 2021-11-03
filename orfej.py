import requests
from datetime import datetime
from bs4 import BeautifulSoup
from destination_data import  DestinationData

class Orfej:
    def __init__(self, destination_data_list):
        URL = 'http://www.pdorfej.com/'
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')

        job_elems = soup.find_all('div', {"class": "content"})
        for job_elem in job_elems:
            try:
                url = job_elem.find('a')['href']
            except Exception as ex:
                continue
            title = job_elem.h2.text.strip()
            button_date = job_elem.find('button').text
            date_str = button_date.replace('Датум:', '').strip()
            # job_elem.text.split('Време')[0].replace('Датум:', '').strip()

            dd = DestinationData()
            dd.url = url
            dd.klub = 'PD Orfej'
            dd.title = title
            dd.date_str = date_str
            dd.date_start, dd.date_end = self._convert_date(dd.date_str)
            if (dd.date_start > datetime.today()):
                destination_data_list.append(dd)


    def __init2__(self, destination_data_list):
        URL = 'http://www.pdorfej.com/'
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')

        results = soup.find('div', {"class": "divTable orangeTableAktuelno"}) #  orangeTableAktuelno
        aktuelno = results.find('div',  {"class": "divTableBody"})

        job_elems = aktuelno.find_all('div', {"class": "divTableRow"})
        for job_elem in job_elems:
            # print(job_elem)
            elem_data = job_elem.find_all('div',  {"class": "divTableCell"})
            e1 = elem_data[0].text.replace('Датум:', '').split('Назив:')
            #print(e1[0])
            #print(e1[1])
            url = elem_data[1].find('a')['href']
            #print(url)
            #print('==========================')

            dd = DestinationData()
            dd.url = url
            dd.klub = 'PD Orfej'
            dd.title = e1[1].strip()
            dd.date_str = e1[0].strip()
            dd.date_start, dd.date_end = self._convert_date(dd.date_str)
            destination_data_list.append(dd)

    def _convert_date(self, date_str):
        # print(date_str)
        d_split = date_str.split('-')
        date1 = d_split[0].split('.')
        date_start = datetime(year=int(date1[2]), month=int(date1[1]), day=int(date1[0]))
        date_end = date_start
        if(len(d_split)==2):
            date1 = d_split[1].split('.')
            date_end = datetime(year=int(date1[2]), month=int(date1[1]), day=int(date1[0]))
        return date_start, date_end
