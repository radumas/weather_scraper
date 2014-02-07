import requests
data = requests.get('http://api.wunderground.com/api/INSERT_KEY_HERE/geolookup/conditions/q/Switzerland/Zurich.json').json()
location = data['location']['city']
temp_c = data['current_observation']['temp_c']
print "Current temperature in %s is: %s C" % (location, temp_c)