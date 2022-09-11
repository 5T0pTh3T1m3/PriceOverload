# für Datensatz erstellen als 1. ausführen
# formatiert alle einzelnen Dateien so, dass nur noch die nötigen Information in diesen vorhanden sind
import json
import os
import sys
from pprint import pprint
from bs4 import BeautifulSoup
import datetime
import random
import time
from matplotlib import pyplot
from multiprocessing import Pool
from functools import partial


def stunde_runden(unixinput):
    return 3600000 * (unixinput // 3600000)


def get_preisdaten(file_path, prodtype):
    extra = None  # eventuelle extra Daten zu dem Produkt (GPU Chipsatz/Netzteil Leistung)
    daten = {}
    '''
    Dateistruktur:
    Dictionary, Key = Zeitpunkt in Unixtime (Sekunden) -> darin ist Liste  Preis zu dem jeweiligen Zeitpunkt und dem jeweiligen Shoplabel
    '''
    file = open(file_path, encoding='UTF-8').read()
    Soup = BeautifulSoup(file, "html.parser")

    # gibt mehrere Male Script in dem HTML-DOC, das letzte enthält das gewollte Script mit den Daten
    wanted = Soup.find_all('script')[-1].text

    # nach allen einzelnen Befehlen von JS Splitten + den mit den Preisdaten raussuchen
    # (kann danach von JSON interpretiert werden)
    wanted = wanted.split(';')
    for element in wanted:
        if 'var chart_data' in element:
            wanted = element.split()[4:]  # falsche Klammern + Variablenennamen müssen entfernt werden

    buffer = wanted.copy()
    wanted = ''
    for element in buffer:
        wanted += element + ' '
    # jetzt ist in Wanted nurnoch die Zeile mit der Variable für die Preisdaten
    preisdaten = json.loads(wanted)
    if len(preisdaten) == 0:
        return None

    if prodtype == 'GPU':
        chipset = Soup.find_all('h2')
        for result in chipset:
            if 'Chipset' in result.text:
                extra = result.text.split(': ')[-1]
                break

    if prodtype == 'PSU':
        chipset = Soup.find_all('p')
        for result in chipset:
            if ' W' in result.text:
                extra = result.text.strip()
                break

    if prodtype == 'CPU':
        chip = Soup.find('h1')
        extra = chip.text
    '''
    Dateistruktur:
    Liste, in dieser sind die Preisdaten der einzelnen Shops vorhanden
    darin Dictionary mit den Keys label, data
    label -> enthält String mit der Shopbezeichnung
    data -> list mit den einzelnen Punkten für Preisdaten, 

    Element in dieser list:
    [zeit in unixtime (Millisekunden), Preis (Cent, wenn nicht verfügbar -> None)]
    '''

    # alle Daten auf einen Tag genau runden
    for zeitpunkt in range(stunde_runden(min([shop['data'][0][0] for shop in preisdaten])), stunde_runden(max([shop['data'][-1][0] for shop in preisdaten])), 3600000):
        # niedrigsten Preis zu diesem Zeitpunkt herausfinden
        preis = []  # enthält alle Shops mit den jeweligen Preisen, danach wird der mit dem Minimum ermittelt
        for shop in preisdaten:
            for datensatz in reversed(shop['data']):
                if stunde_runden(datensatz[0]) <= zeitpunkt + 3600000:
                    preis.append([datensatz[1], shop['label']])
                    break

        if len(daten.keys()) != 0:
            minpreis = [daten[zeitpunkt - 3600000][0], daten[zeitpunkt - 3600000][1]]
        else:
            minpreis = [None, None]
        for shop in preis:
            if minpreis[1] is shop[1]:  # wie sich der bisher günstigste Shop entwickelt hat
                minpreis = shop.copy()
            elif minpreis[0] is None and shop[0] is not None:  # wenn es jetzt verfügbar ist vorher aber nicht war
                minpreis = shop.copy()
            elif minpreis[0] is not None and shop[0] is not None:  # ob es jetzt einen günstigeren Shop gibt
                if minpreis[0] > shop[0]:
                    minpreis = shop.copy()
        daten.update({zeitpunkt: minpreis})
    return [daten, extra]


def filter_preisdaten(source_file, dest_file, prodtype):
    data = get_preisdaten(source_file, prodtype)
    if data is not None:
        open(dest_file, 'w').write(json.dumps(data))


# eingabe = [source_path, destination_path, GPU, PSU, filerange, processindex, cpu]
# filtert die Dateien in einem bestimmten Bereich
def mp_filtering(eingabe):
    files = sorted(os.listdir(eingabe[0]))
    for i in eingabe[3]:
        if i < len(files):
            try:
                filter_preisdaten(eingabe[0] + files[i], eingabe[1] + files[i].split('.')[0] + '.json', eingabe[2])
            except Exception as e:
                print(e)
                print(files[i])
                try:
                    open('neuFiltern/' + str(eingabe[4]), 'a').write(files[i] + '\n')
                except FileNotFoundError:
                    open('neuFiltern/' + str(eingabe[4]), 'w').write(files[i] + '\n')


if __name__ == '__main__':
    p = Pool()
    source = 'C:/Users/PC/Daten/daten/Code/BWKI/daten/Preisdaten/GPU/'
    destination = 'neuFiltern/GPU/'
    NumberOfProcesses = 12
    Numbers = [[] for i in range(NumberOfProcesses)]  # die Indexe der Aufgaben für jeden Prozess
    for i in range(len(os.listdir(source))):
        Numbers[i % NumberOfProcesses].append(i)

    data = [[source, destination, 'GPU', Numbers[i], i].copy() for i in range(NumberOfProcesses)]
    p.map(mp_filtering, data)

    p.close()
    p.join()
