import requests
import xml.etree.ElementTree as ET

ICAO_CODE = 'LKTB'
#tree = ET.parse('')
#root = tree.getroot()
DATA_SOURCE = 'https://aviationweather.gov/adds/dataserver_current/httpparam?dataSource=metars&requestType=retrieve&format=xml&stationString=LKTB,%20PHNL&hoursBeforeNow=2'.format(ICAO_CODE)

def main():
    response = requests.get(DATA_SOURCE)

    tree =  ET.fromstring(response.content)
    for element in tree.findall('//data/METAR'):
        time = element.find('./observation_time').text
        temp = element.find('./temp_c').text
        print('{} - {}'.format(time, temp))

if __name__ == '__main__':
    main()