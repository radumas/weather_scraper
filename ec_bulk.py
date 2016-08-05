#!/usr/bin/python3
import os 
import xml.etree.ElementTree as et
from datetime import date

def nullfloat(x):
    if not x:
        return None
    return float(x)

os.chdir("/home/rad/Desktop/Research Analyst Assignment/Toronto_weather_data")
e = et.parse('eng-daily-01012015-12312015.xml').getroot()

rows = []

for elem in e.findall('stationdata'):
    attribs = elem.attrib
    row = {}
    row['weather_date'] = date(int(attribs['year']),int(attribs['month']),int(attribs['day']))
    row['maxtemp'] = nullfloat(elem.find('maxtemp').text)
    row['meantemp'] = nullfloat(elem.find('meantemp').text)
    row['mintemp'] = nullfloat(elem.find('mintemp').text)
    row['totalprecip'] = nullfloat(elem.find('totalprecipitation').text)
    row['totalrain'] = nullfloat(elem.find('totalrain').text)
    row['totalsnow'] = nullfloat(elem.find('totalsnow').text)
    row['snowonground'] = nullfloat(elem.find('snowonground').text)
    rows.append(row)

from pgdb import connect
con = connect(database='rad',host='localhost:5432',user='python',password='py')
cursor = con.cursor()

cursor.executemany("INSERT INTO public.toronto_weather_ec_daily("
            "weather_date, maxtemp, meantemp, mintemp, totalprecip, totalsnow, "
            "totalrain, snowonground)"
    "VALUES (%(weather_date)s, %(maxtemp)s, %(meantemp)s, %(mintemp)s, %(totalprecip)s, %(totalsnow)s, "
            "%(totalrain)s, %(snowonground)s)", rows)
con.commit()