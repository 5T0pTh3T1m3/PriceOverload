# für Datensatz erstellen als 6. ausführen
# formatiert den kompletten Datensatz erneut -> jetzt sind Trends darin gespeichert
'''
neue Dateistruktur für die Preise:
names[i] = 'ein Produktname',
zeiten = alle Zeiten (gehen jetzt nurnoch von Tag 100 bis Tag 600 bzw. 650 bzw. 670, von Variante abhängig)
preise = [
    [
        [preis 1 vor 10 Tagen, preis 2 vor 10 Tagen],
        [preis 1 vor 09 Tagen, preis 2 vor 09 Tagen],
        ...
        [preis 1 vor 00 Tagen, preis 2 vor 00 Tagen],
    ]
...],
trends = [
    [trend produkt 1 für preisdaten 1 (nächsten n Tage avg), trend produkt 2],
    [trend produkt 2 für preisdaten 2 (nächsten n Tage avg), trend produkt 2]
    ...
]
scales = [
    [
        {info: "m = max_x - min_x, n = 1 - (m * max_x), x = (1-n)/m",
        max_x: 42,
        min_x: 23
        }
    ...
]
'''
import json


def avg(LISTE):
    return sum(LISTE)/len(LISTE)


# trenddauer = so viele Tage vorausschauend soll der Trend sein
def format_file(file, trenddauer):
    content = json.loads(open(file).read())
    preise_neu = []
    trends = []
    zeiten_neu = []

    # nur den Bereich durchgehen, welcher komplette Daten enthält (sowohl vorne als auch hinten)
    for i in range(trenddauer, len(content['zeiten']) - trenddauer):
        zeiten_neu.append(content['zeiten'][i])

        preise_neu.append([])
        # alle Preise für Verlauf von der Vergangenheit aus Sicht von i
        for j in range(i - trenddauer, i):
            preise_neu[-1].append(content['preise'][j])

        # wird später einfach in den Trend für den jeweiligen Preis eingesetzt
        trend = []
        for j in range(len(content['names'])):  # durch alle Produkte durchgehen, Trend für jeweiliges Produkt berechnen
            trend.append(avg([content['preise'][k][j] for k in range(i, i + trenddauer)]) <= content['preise'][i][j])
        trends.append(trend)

    content['preise'] = preise_neu
    content.update({'trends': trends})
    content['zeiten'] = zeiten_neu
    return content


stuff = [20, 50, 100]
for TRENDDAUER in stuff:
    neu = format_file('FINISHED.json', TRENDDAUER)
    open(f'DatenMitTrendsDrin/{TRENDDAUER}.json', 'w').write(json.dumps(neu))
