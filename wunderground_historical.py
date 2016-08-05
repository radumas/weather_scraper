import requests
import json
from pgdb import connect

def nullfloat(x):
    if not x:
        return None
    return float(x)

def get_precip(gooddate):
    urlstart = 'http://api.wunderground.com/api/f3bd6ae3f61cbf1b/history_'
    urlend = '/q/Canada/Toronto.json'

    url = urlstart + str(gooddate) + urlend
    data = requests.get(url).json()
    
    for_date = date(int(data['history']['date']['year']),int(data['history']['date']['mon']),int(data['history']['date']['mday']))

    
    cursor.execute("INSERT INTO toronto_weather_json (for_date, weather) VALUES (%s, %s)", (for_date, json.dumps(data),))
    con.commit()
    
    for summary in data['history']['dailysummary']:
        precip = nullfloat(summary['precipm'])
        snow = nullfloat(summary['snow'])
        snowfall = nullfloat(summary['snowfallm'])
        snowdepth = nullfloat(summary['snowdepthm'])
        maxtemp = nullfloat(summary['maxtempm'])
        meantemp = nullfloat(summary['meantempm'])
        mintemp = nullfloat(summary['mintempm'])
        fog = nullfloat(summary['fog'])
        rain = nullfloat(summary['rain'])
        thunder = nullfloat(summary['thunder'])
        cursor.execute("INSERT INTO public.toronto_weather("
            "for_date, precip, snow, snowfall, snowdepth, maxtemp, meantemp, "
            "mintemp, fog, rain, thunder)"
            "VALUES (%s, %s, %s, %s, %s, %s, %s, "
            "%s, %s, %s, %s)", (for_date, precip, snow, snowfall, snowdepth, maxtemp, meantemp, mintemp, fog, rain, thunder, ))
        con.commit()
    cursor.close()
    
if __name__ == "__main__":
    from datetime import date
    from dateutil.relativedelta import relativedelta
    con = connect(database='rad',host='localhost:5432',user='python',password='py')
    cursor = con.cursor()
    
    cursor.execute("SELECT max(for_date) FROM toronto_weather")
    b = cursor.fetchone().max + relativedelta(days=+1)
    get_precip(b.strftime("%Y%m%d"))