from openpyxl import Workbook
from datetime import date

from pk_radnicki import PkRadnicki
from krug import Krug
from alticlub import AltiClub
from kopaonik import Kopaonik
from azimut import Azimut
from pk_balkan import PkBalkan
from pancic import Pancic
from orfej import Orfej
from avanturisti import Avanturisti
from pobeda import Pobeda
from zeleznicar import Zeleznicar
from avala import Avala

print('Nemoguce obraditi:')
print(' - http://www.jelenak.rs/plan2020.pdf  Pancevo')

print('')
print('Tesko za obradu:')
print(' - http://soko.rs/category/najava_akcija/  Pancevo')
print(' - http://pddorcol.rs/  ZASTARELO')
print(' - http://www.pdptt.rs/plan-akcija/  vidi kalendar')

# TODO
# http://pddorcol.rs/  zastarelo
# http://www.pdptt.rs/plan-akcija/
# https://www.facebook.com/pk.slavija/events/?ref=page_internal i http://pk-slavija.in.rs/
# http://soko.rs/category/najava_akcija/


list_destinations = []
print("Avala")
Avala(list_destinations)
print("Radnicki")
PkRadnicki(list_destinations)
print("Krug")
Krug(list_destinations)
print("Alti")
AltiClub(list_destinations)
print("Kopaonik")
Kopaonik(list_destinations)
print("Azimut")
Azimut(list_destinations)
print("Balkan")
PkBalkan(list_destinations)
print("Pancic")
# UPOZORENJE PANCIC JE SKROZ PROMENIO SAJT, ISKLJUCEN DO AZURIRANJA KODA
Pancic(list_destinations)
print("Orfej")
Orfej(list_destinations)
print("Avanturisti")
Avanturisti(list_destinations)
print("Pobeda")
Pobeda(list_destinations)
print("Zeleznicar")
Zeleznicar(list_destinations)


wb = Workbook()
ws = wb.active
header = ['Klub', 'Naslov', 'Polazak', 'Povratak', 'Link', 'Opis']
ws.append(list(header))
for items in list_destinations:
    ws.append(list(items))

today = date.today().strftime('%d-%m-%Y')
file_name = 'akcije_posle_' + today + '.xlsx'
wb.save(file_name)
