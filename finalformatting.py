# für Datensatz erstellen als 5. ausführen
# führt die Preiskurven von den verschiedenen Produkten zu einem Array mit allen Preiskurven zusammen
import json
import sys
import time


def format_file(sourcefile):
    content = json.loads(open(sourcefile, encoding='UTF-8').read())
    start = time.time()

    bezeichnungen = []
    zeiten = []
    preise = []
    skalierungen = []

    # alle Zeitpunkte, die möglich sind einfügen
    # als Minimum kann man irgendeine GPU nehmen (sonst wird IBM mit Daten von vor 2000 Jahren genommen....)
    zeitpunkte = [int(zeit) for zeit in content['GeForce GTX 1650 G5'].keys() if zeit != 'scale']
    begin = min(zeitpunkte)
    end = max(zeitpunkte)
    del zeitpunkte

    for zeit in range((begin//86400000) * 86400000, (end//86400000) * 86400000, 86400000):
        zeiten.append(zeit)
        preise.append([None for i in range(len(content.keys()))])  # alle Produkte auf N.A. setzen

    remaining = len(content.keys())
    done = 0
    # allen Zeitpunkte die Produkte zuordnen
    for product in content.keys():
        bezeichnungen.append(product)
        # gesamte Zeit durchgehen
        # for zeit in range((begin//86400000) * 86400000, (end//86400000) * 86400000, 86400000):
        for zeit in zeiten:
            preis = None  # Preis von dem Produkt, zu dem Zeitpunkt
            # alle Preise innerhalb von dem Tag durchgehen (sehr ineffizient, weil auf Millisekunde genau, sollte aber gehen)
            for zeit2 in range(zeit, zeit + 86400000, 10000):
                if str(zeit2) in content[product].keys():
                    if preis is None:
                        preis = content[product][str(zeit2)]
                    elif content[product][str(zeit2)] is not None:
                        if content[product][str(zeit2)] < preis:
                            preis = content[product][str(zeit2)]

            if preis is None:
                preis = 0
            preise[zeiten.index(zeit)][bezeichnungen.index(product)] = preis
        try:
            skalierungen.append(content[product]['scale'])
        except KeyError:
            print(content[product])
            sys.exit()

        done += 1
        if done % 20 == 1:
            print(f'avg Secs. per Product: {(time.time() - start)/done}s')
            print(f'Time Remaining: {(((time.time() - start)/done) * (remaining - done))/60}min')
            print(f'{(done/remaining) * 100}% done...')
            print(f'Script running since {time.time() - start}s now')
            print('------------------------------------------------')
    return {'names': bezeichnungen, 'zeiten': zeiten, 'preise': preise, 'scales': skalierungen}


open('FINISHED.json', 'w').write(json.dumps(format_file('ALLES.json')))
# open('test.json', 'w').write(json.dumps(format_file('konstantePreise.json')))
