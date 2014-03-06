import requests
def get_precip(gooddate):
    urlstart = 'http://api.wunderground.com/api/INSERT_KEY_HERE/history_'
    urlend = '/q/Switzerland/Zurich.json'

    url = urlstart + str(gooddate) + urlend
    data = requests.get(url).json()
    for summary in data['history']['dailysummary']:
        print ','.join((gooddate,summary['date']['year'],summary['date']['mon'],summary['date']['mday'],summary['precipm'], summary['maxtempm'], summary['meantempm'],summary['mintempm']))

if __name__ == "__main__":
    from datetime import date
    from dateutil.rrule import rrule, DAILY

    a = date(2013, 1, 1)
    b = date(2013, 12, 31)

    for dt in rrule(DAILY, dtstart=a, until=b):
        get_precip(dt.strftime("%Y%m%d"))