# für Datensatz erstellen als 4. ausführen
# skaliert alle Preise, sodass sie zwischen 0 und 1 liegen
import json
import sys


# skaliert alle Dateien, sodass sie zwischen 0 und 1 liegen
# -> es wird eine lineare Funktion erstellt, durch welche das Minimum >0 und das Maximum bei 1 ist
# in der Datei für ein Produkt, wird jeweils die Skalierung gespeichert
# als INPUT wird eine komplette Datei genommen, die bereits fertig klassifiziert wurde
def scale_data(sourcefile, targetfile):
    content = json.loads(open(sourcefile).read())

    for cat in content.keys():
        if 'scale' not in content[cat].keys():  # -> kann auch teilweise skalierte Datei übergeben werden
            # Funktion berechnen, welche die Werte skalieren soll
            buffer = [float(content[cat][zeit]) for zeit in content[cat].keys() if content[cat][zeit] is not None]
            max_x = max(buffer)
            min_x = min(buffer)
            try:
                m = 0.9999/(max_x - min_x)  # Delta Y / Delta X (minimaler Wert für Y > 0, 0 heißt Produkt N.A.)
                n = 1 - (m * max_x)
            except ZeroDivisionError:  # maximum und minimum sind identisch -> einfach so skalieren, dass es dauerhaft 1 ist
                m = 1
                n = 1 - max_x

            # alle Preise skalieren
            for zeit in content[cat].keys():
                if content[cat][zeit] is not None:
                    content[cat][zeit] = (m * float(content[cat][zeit])) + n

            # Skalierung speichern
            content[cat].update({'scale': {'info': 'm = 0.9999/(max_x - min_x), n = 1 - (m * max_x), x = (y-n)/m', 'max_x': max_x, 'min_x': min_x}})
    open(targetfile, 'w', encoding='UTF-8').write(json.dumps(content))


scale_data('ALLES.json', 'ALLES.json')
