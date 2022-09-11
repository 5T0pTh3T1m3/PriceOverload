# passt Daten von YahooFinance an die Struktur der restlichen Daten an
import datetime
import json
import os
import sys


def format_timestamp(date):
    return int(datetime.datetime.timestamp(datetime.datetime.strptime(date.replace('-', ''), '%Y%m%d')) * 1000)


# liest den die Datei einer Kryptowährung ein, passt Format dem der anderen Daten an
def format_crypto_course(source_path, source_file, dest_path, dest_file):
    data = open(source_path + source_file).read().replace('\n', ',').split(',')
    formatted_data = [source_file.split('.')[0], {}]
    '''
    angestrebtes Format:
    list = [währung, preisverlauf]
        preisverlauf[zeitpunkt] = preis
    '''
    places = {'date': 0, 'close': 4}
    # bei 7 beginnen (erste Zeile sind die Attribute in plain), in 7 Schritten (allen Zeilen einzeln durchgehen)
    for i in range(7, len(data), 7):
        if data[i + places['date']] != '' and data[i + places['close']] != '':
            try:
                formatted_data[1].update({format_timestamp(data[i + places['date']]): data[i + places['close']]})
            except OSError:  # eine Zeit vor 1970 wurde angegeben (in Unix Time unmöglich)
                pass
            except Exception as e:
                print(e)
                print(source_file)
                sys.exit()
    open(dest_path + dest_file, 'w', encoding='UTF-8').write(json.dumps(formatted_data))


path = 'andereDaten/Aktien/'

for file in os.listdir(path):
    format_crypto_course(path, file, 'fertigeDateien/', file.split('.')[0] + '.json')
