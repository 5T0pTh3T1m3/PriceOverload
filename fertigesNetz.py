import random
import json
import datetime
import time


# TODO: durch das eigentliche Netz ersetzen
def netz(eingabe):
    return [bool(random.randrange(0, 2)) for i in range(len(eingabe[-1]))]


# alle Produkte inklusive Index anzeigen lassen
def list_products_with_index(products):
    print('----------\nIndex, Name')
    for product in products:
        if len(str(products.index(product))) == 1:
            print(f'    {products.index(product)}, {product}')
        elif len(str(products.index(product))) == 2:
            print(f'   {products.index(product)}, {product}')
        elif len(str(products.index(product))) == 3:
            print(f'  {products.index(product)}, {product}')
    print('Ende\n----------')


# lässt einen Nutzer Produkt, Datum und Trendlänge auswählen
def get_userinput(path):
    # ermitteln, welche Kategorie gewählt werden soll
    while True:
        trenddauer = input('Bitte gib die Trenddauer in Tagen ein (20, 50 oder 100)\n(nur die Zahl)\n')
        if trenddauer in ['20', '50', '100']:
            print(f'Trenddauer von {trenddauer} Tagen erfolgreich eingegeben')
            break

    database = json.loads(open(path + trenddauer + '.json').read())
    product = None

    # genaues Produkt ermitteln
    while True:
        search_query = input('Bitte gib einen Suchbegriff für ein Produkt ein (alle Produkte die diesen im Name enthalten werden angezeigt)\n'
                             'Netzteile habe ihre Wattzahl auf 100W genau als Namen (bsp. 500)\n')
        results = [name for name in database['names'] if search_query in name]
        if len(results) == 0 or search_query == '':  # zu viele/wenige Produkte wurden gefunden
            if input(f'dein Suchbegriff wurde nicht gefunden, möchtest du in einer Liste aller ({len(database["names"])}) Produkte suchen?(y/n)\n') not in ['Y', 'y']:
                continue
            else:
                results = database['names']
        list_products_with_index(results)
        searchedproduct = input('Gib bitte den Index für das gesuchte Produkt ein (leer lassen wenn nicht vorhanden)\n')
        try:
            if input(f'Ist das Produkt {results[int(searchedproduct)]} richtig (y/n)\n') in ['Y', 'y']:
                product = results[int(searchedproduct)]
                break
        except ValueError:
            if searchedproduct != '':
                print(f'{searchedproduct} ist kein Index für ein Produkt (falsche Zahl oder gar keine Zahl)')
                print('Beginne bitte von vorne')
        except IndexError:
            if searchedproduct != '':
                print(f'{searchedproduct} ist kein Index für ein Produkt (falsche Zahl oder gar keine Zahl)')
                print('Beginne bitte von vorne')

    # Zeitpunkt der Betrachtung ermitteln
    while True:

        beginn = (str(datetime.datetime.utcfromtimestamp(min([zeit for zeit in database['zeiten']])//1000)).split()[0]).split('-')
        ende = (str(datetime.datetime.utcfromtimestamp(max([zeit for zeit in database['zeiten']])//1000)).split()[0]).split('-')

        datum = input('bitte gebe ein Datum innerhalb von diesem Zeitraum an:\n'
                      f'{beginn[2] + "-" + beginn[1] + "-" + beginn[0]}\n'
                      f'{ende[2] + "-" + ende[1] + "-" + ende[0]}\n'
                      '(dd-mm-yyyy)\n')

        try:
            # +3600000 wegen der Zeitzone
            unix_datum = int(datetime.datetime.strptime(datum, "%d-%m-%Y").timestamp() * 1000) + 3600000
            bereich = range(min([zeit for zeit in database['zeiten']]), max([zeit for zeit in database['zeiten']]) + 1)
            if unix_datum not in bereich:
                print(f'das Datum {datum} ist nicht innerhalb von dem gegebenen Zeitrahmen, gib es bitte erneut ein')
            elif input(f'ist das Datum {datetime.datetime.utcfromtimestamp(unix_datum//1000).date()} richtig(y/n)?\n') in ['Y', 'y']:
                unix_datum = (unix_datum//864000000) * 864000000  # auf ganze Tage runden
                break
        except ValueError:
            print(f'falsches Format bei der Eingabe "{datum}"')

    print(f'Daten für das Produkt {product} mit der Trenddauer {trenddauer} vom {datum} werden gesucht...')
    productindex = database['names'].index(product)  # wo befindet sich das Produkt in allen Listen
    print(database['scales'][productindex])


get_userinput('DatenMitTrendsDrin/')
