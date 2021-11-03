import requests
# import re
from datetime import datetime
from bs4 import BeautifulSoup
from destination_data import  DestinationData

class Krug:
    def __init__(self, destination_data_list):
        URL = 'http://pdkrug.org.rs/aktuelne-akcije/'
        headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0",
                   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"}

        page = requests.get(URL, headers=headers)

        soup = BeautifulSoup(page.content, 'html.parser')

        results = soup.find('main', id='main') # .find('div',{"class": "elementor-widget-container"})

        # results = soup.find('div', id='content') #.find('div',{"class": "elementor-widget-wrap"})
        job_elems = results.find_all('div', {"class": "elementor-text-editor elementor-clearfix"}) # ('section')
        # del job_elems[0]

        for job_elem in job_elems:
            try:
                #print(job_elem)
                url = ''
                title = ''
                link_elem = job_elem.find('a')
                if (link_elem != None):
                    url = link_elem['href']
                    title = link_elem.text.strip()
                    p_tags = job_elem.find_all('p')
                    desc_elem = p_tags[1].text
                    date_start_str = job_elem.find('em').text.strip()


                    #print(url)
                    #print(title)
                    #print(desc_elem)
                    #print(date_start_str)

                    dd = DestinationData()
                    dd.klub = 'Krug'
                    dd.url = url
                    dd.title = title
                    dd.desc = desc_elem

                    try:
                        dd.date_start, dd.date_end = self._convert_date(date_start_str)
                    except:
                        date_elems = job_elem.find_all('em')
                        date_start_str = ''
                        for date_elem in date_elems:
                            date_start_str = date_start_str + date_elem.text
                        dd.date_start, dd.date_end = self._convert_date(date_start_str)
                    dd.date_str = date_start_str

                    if(dd.date_start > datetime.now()):
                        destination_data_list.append(dd)

                #print('======================================')
                #date_start_str = job_elem.find('td',{"class": "list-date small"}).text.strip()
                #url = ''
                #title = ''
                #link_elem = job_elem.find('a')
                #if(link_elem != None):
                #    url = link_elem['href']
                #    title = link_elem.text.strip()
                #desc_elem = job_elem.text.replace(date_start_str, '').replace('Link', '')
                # print(date_start_str, desc_elem, url)

                # dd = DestinationData()
                #dd.url = 'https://www.psd-kopaonik.org.rs/' + url
                #dd.title = title
                #dd.desc = desc_elem
                #dd.date_start = date_start_str
                #dd.date_end = date_start_str  # menjaj

                #destination_data_list.append(dd)
            except Exception as e:
                print(e)
                pass

    def _convert_date(self, date_str):
        meseci = ['januar', 'februar', 'mart', 'april', 'maj', 'jun', 'jul',
                  'avgust', 'septembar', 'oktobar', 'novembar', 'decembar']
        # print(date_str)

        #regex = re.compile(".*?\((.*?)\)")
        #regex_result = re.findall(regex, date_str)
        #date_str_clean = date_str.replace(regex_result[0], '').replace('()', '')

        date_str_arr = date_str.replace(' godine', '').replace('.', '').split(' ')

        date_start = None
        date_end = None
        godina = int(date_str_arr[2]) # int(date_str_clean[-12:][:4])
        mesec1 = 0
        mesec2 = 0
        dan1 = 0
        dan2 = 0
        # print('godina: ', str(godina))
        dani = date_str_arr[0]  #date_str_clean[:-13].replace('.', '')
        dani_split = dani.split('-')
        if(len(dani_split) == 2):
            # print(dani_split[0], ' iiii... ', dani_split[1])
            res1 = [elem for elem in meseci if (elem in dani_split[0])]
            res2 = [elem for elem in meseci if (elem in dani_split[1])]
            mesec2 = meseci.index(date_str_arr[1]) + 1 # meseci.index(res2[0]) + 1
            dan2 = int(dani_split[1]) # int(dani_split[1].replace(res2[0], ''))
            if (bool(res1)):
                mesec1 = meseci.index(res1[0])+1
                dani_split[0] = dani_split[0].replace(res1[0], '')
            else:
                mesec1 = mesec2
            dan1 = int(dani_split[0])
        else:
            # print(dani)
            # res = [elem for elem in meseci if (elem in dani)]
            mesec1 = meseci.index(date_str_arr[1]) + 1 # meseci.index(res[0])+1
            mesec2 = mesec1
            # dani = dani.replace(res[0], '')
            dan1 = int(dani)
            dan2 = dan1

        date_start = datetime(year=godina, month=mesec1, day=dan1)
        date_end = datetime(year=godina, month=mesec2, day=dan2)
        return date_start, date_end