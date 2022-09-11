# für Datensatz erstellen als 2. ausführen
# alle Produkte einer Kategorie werden zusammengefasst (alle 3070, 500W Netzteil, etc.)
import sys
from matplotlib import pyplot
import os
import json
from pprint import pprint


CATEGORIES  = {}
'''
Datenstruktur:
categories[wattage oder GPU_Chipset] = [alle GPUs/Netzteile zur category]
'''
DATA = {}
'''
Datenstruktur:
DATA[categorie] = {zeitpunkt: preis}
'''


# die Produkt nach Kategorien sortieren
def sort_into_categories(path, file, categories, filetype):
    if '._' not in file:
        data = json.loads(open(path + file, encoding='UTF-8').read())
        if filetype == 'PSU':
            if len(data[1].split()) == 2:  # alle rausfiltern die nicht im richtigen Format gespeichert wurden
                data[1] = data[1].split()
                try:
                    data[1][0] = int(data[1][0])
                    for c in categories.keys():
                        if data[1][0] in range(c - 50, c + 49):
                            categories[c].append([file, data])
                except:
                    print('Problem bei: ' + file + f'!\n{data[1][0]} ist kein Integer!')
            else:
                print('WRONG FORMAT IN FILE: ' + file)
        if filetype == 'GPU':
            if data[1] not in categories.keys():
                if data[1] is not None:
                    categories.update({data[1]: [[file, data.copy()]]})
            else:
                categories[data[1]].append([file, data.copy()])
    return categories.copy()


def extract_data(categories):
    '''
    Datenstruktur:
    DATA[categorie] = {zeitpunkt: preis}
    '''
    data = {}
    for cat in categories.keys():
        if len(categories[cat]) != 0:
            preisverlauf = {}
            '''
            preisverlauf Datenstruktur:
            preisverlauf[zeitpunkt] = preis

            product Datenstruktur:
            liste[dateiname, dateiinhalt]
                dateiinhalt:
                liste[dict {preisdaten}, categorie]
                    preisdaten:
                        list[zeitpunkt] = [preis, shop]
            '''
            for product in categories[cat]:
                for zeitpunkt in product[1][0].keys():
                    if zeitpunkt in preisverlauf.keys():  # Zeitpunkt ist bereits vorhanden
                        if preisverlauf[zeitpunkt] is None:  # war in dem Moment nicht verfügbar
                            preisverlauf[zeitpunkt] = product[1][0][zeitpunkt][0]
                        elif product[1][0][zeitpunkt][0] is not None:
                            if preisverlauf[zeitpunkt] > product[1][0][zeitpunkt][0]:  # war in dem Moment vorhanden, aber teurer
                                preisverlauf[zeitpunkt] = product[1][0][zeitpunkt][0]
                    else:
                        preisverlauf.update({zeitpunkt: product[1][0][zeitpunkt][0]})
            data.update({cat: preisverlauf})
    return data


# einfach einmal mit den Parametern ausführen, enstehende Datei ist zu groß für GitHub
def cpus_klassifizieren(sourcepath, targetfile):
    categories = {}
    for file in os.listdir(sourcepath):
        productdata = json.loads(open(sourcepath + file, encoding='UTF-8').read())
        buffer = {}
        for zeitpunkt in productdata[0].keys():
            buffer.update({zeitpunkt: productdata[0][zeitpunkt][0]})
        categories.update({productdata[1]: buffer})
    open(targetfile, 'w', encoding='UTF-8').write(json.dumps(categories))


def visualize_data(xaxis, yaxis):
    pyplot.plot(xaxis)
    pyplot.ylabel(yaxis)
    pyplot.show()


'''PSU = True
if PSU:
    # 100 bis 1600 Watt sind möglich (16 * 100)
    for i in range(1, 17):
        CATEGORIES.update({i * 100: []})
        DATA.update({i * 100: {}})
PATH = 'neuFiltern/GPU/'

for file in os.listdir(PATH):
    CATEGORIES = sort_into_categories(PATH, file, CATEGORIES, 'GPU')

DATA = extract_data(CATEGORIES)
open('fertigeDateien/GPU.json', 'w', encoding='UTF-8').write(json.dumps(DATA))'''

cpus_klassifizieren('neuFiltern/CPU/', 'fertigeDateien/CPU.json')
