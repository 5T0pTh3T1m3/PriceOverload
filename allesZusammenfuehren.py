# für Datensatz erstellen als 3. ausführen
# nimmt mehrere Dateien in vorherigem Format (CPU/GPU/... getrennt) -> fügt alle zu einer Datei zusammen
import os
import sys
import json


# fügt zu Bigfile die Produkte in SmallFile hinzu
def add_to_file(bigcontent, smallcontent, variante):
    '''
    bigcontent[product] = {
        zeit: skalierter_preis,
        scale:{
            info: m = max_x - min_x, n = 1 - (m * max_x), x = (1-n)/m,
            max_x: int,
            min_x: int
        }
    }
    '''
    '''
    Variante 0 (bei Daten von YahooFinance)
    smallcontent = [
        Name,
        {
            zeit: unskalierter Preis
        }
    ]
    Variante 1 (bei Daten von pcpartpicker.com (bereits komplett aufbereitet))
    smallcontent[product] = {
        zeit: skalierter_preis,
        scale:{
            info: m = max_x - min_x, n = 1 - (m * max_x), x = (1-n)/m,
            max_x: int,
            min_x: int
        }
    }
    '''

    if variante == 1:
        # einfach das Gesamte in die große Variable einfügen (hat schließlich bereits richtige Struktur)
        for product in smallcontent.keys():
            bigcontent.update({product: smallcontent[product]})
        return bigcontent
    elif variante == 0:
        buffer = smallcontent[1]
        # enthält Daten in der richtigen Struktur, aber ohne Skalierung -> können später in Skalieren.py skaliert werden
        data = {}
        for zeit in buffer.keys():
            data.update({zeit: buffer[zeit]})
        bigcontent.update({smallcontent[0]: data})
        return bigcontent


path = 'fertigeDateien/'
bigfile = 'GPU.json'
BigContent = json.loads(open(path + bigfile).read())

for smallfile in os.listdir(path):
    if smallfile != 'GPU.json':
        SmallContent = json.loads(open(path + smallfile).read())
        if smallfile not in ['GPU.json', 'CPU.json', 'PSU.json']:
            Variante = 0
        else:
            Variante = 1
        BigContent = add_to_file(BigContent, SmallContent, Variante)

open('ALLES.json', 'w').write(json.dumps(BigContent))
