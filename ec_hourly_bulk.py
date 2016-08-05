#!/usr/bin/python3
import xml.etree.ElementTree as et
from datetime import date, datetime
import requests
import traceback

def nullfloat(x):
    if not x:
        return None
    if x.isspace():
        return None
    return float(x)

def nullsplit(string):
    if not string:
        return None
    if string == "NA":
        return None
    if string.isspace():
        return None
    return str.split(string,',')

def parse_ec_hourly(xml):
    e = et.fromstring(xml)

    rows = []
    i = 0

    for elem in e.findall('stationdata'):
        i = i + 1
        attribs = elem.attrib
        row = {}
        try:
            row['weather_time'] = datetime(int(attribs['year']),int(attribs['month']),int(attribs['day']),int(attribs['hour']))
            row['temperature'] = nullfloat(elem.find('temp').text)
            row['wind_dir'] = nullfloat(elem.find('winddir').text)
            row['wind_spd'] = nullfloat(elem.find('windspd').text)
            row['weather'] = nullsplit(elem.find('weather').text)
        except ValueError:
            print("Error in observation for ", row['weather_time'])
            print(traceback.format_exc)
            raise SystemExit(0)
        rows.append(row)
        
    return rows

def insert_rows(rows, con, cursor):
    cursor.executemany("INSERT INTO public.toronto_bb_weather_ec_hourly(weather_time, temperature, wind_dir, wind_spd, weather)"
        "VALUES (%(weather_time)s, %(temperature)s, %(wind_dir)s, %(wind_spd)s, %(weather)s)", rows)
    con.commit()
    
if __name__ == "__main__":
    from pgdb import connect
    
    for i in range(1,13):
        #station = 51459
        station = 48549
        url = "http://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=xml&stationID={stationID}&Year=2015&Month={month}&timeframe=1&submit=%20Download+Data".format(month=i,stationID=station)
        print("Getting data for 2015-{month}".format(month=i))
        data = requests.get(url).text
        print("Processing xml")
        rows = parse_ec_hourly(data)
        con = connect(database='rad',host='localhost:5432',user='python',password='py')
        cursor = con.cursor()
        print("Sending processed xml to database")
        insert_rows(rows, con, cursor)