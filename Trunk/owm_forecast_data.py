#Weather forecast from open weather map
import urllib.request
from xml.dom import minidom

url = 'http://api.openweathermap.org/data/2.5/forecast/daily?q=Trondheim&mode=xml&units=metric&cnt=10'

dom = minidom.parse(urllib.request.urlopen(url))
forecast = dom.getElementsByTagName('forecast')[0]

raw_forecasts = []
dated_forecast = {}
dates = []

for node in forecast.getElementsByTagName('time'):
    symbol      = node.getElementsByTagName('symbol')[0]
    precip      = node.getElementsByTagName('precipitation')[0]
    windDir     = node.getElementsByTagName('windDirection')[0]
    windSpeed   = node.getElementsByTagName('windSpeed')[0]
    temp        = node.getElementsByTagName('temperature')[0]
    pressure    = node.getElementsByTagName('pressure')[0]
    humidity    = node.getElementsByTagName('humidity')[0]
    date = node.getAttribute('day')
    
    raw_forecasts.append({
        'date'          : date,
        'from'          : '',
        'to'            : '',
        'symbol'        : symbol.getAttribute('name'),
        'precipitation' : precip.getAttribute('value'),
        'wind_dir'      : windDir.getAttribute('deg'),
        'wind_speed'    : windSpeed.getAttribute('mps'),
        'temperature'   : '',
        'temp_min'      : temp.getAttribute('min'),
        'temp_max'      : temp.getAttribute('max'),
        'pressure'      : pressure.getAttribute('value'),
        'humidity'      : humidity.getAttribute('value')
    })
    if date in dates:
		dated_forecast[date].append({
			'from'          : '',
			'to'            : '',
			'symbol'        : symbol.getAttribute('name'),
			'precipitation' : precip.getAttribute('value'),
			'wind_dir'      : windDir.getAttribute('deg'),
			'wind_speed'    : windSpeed.getAttribute('mps'),
			'temperature'   : '',
            'temp_min'      : temp.getAttribute('min'),
            'temp_max'      : temp.getAttribute('max'),
			'pressure'      : pressure.getAttribute('value'),
            'humidity'      : humidity.getAttribute('value')
		})
    else:
		dates.append(date)
        	dated_forecast[date] = []
		dated_forecast[date].append({
			'from'          : '',
			'to'            : '',
			'symbol'        : symbol.getAttribute('name'),
			'precipitation' : precip.getAttribute('value'),
			'wind_dir'      : windDir.getAttribute('deg'),
			'wind_speed'    : windSpeed.getAttribute('mps'),
			'temperature'   : '',
            'temp_min'      : temp.getAttribute('min'),
            'temp_max'      : temp.getAttribute('max'),
			'pressure'      : pressure.getAttribute('value'),
            'humidity'      : humidity.getAttribute('value')
		})

for date in dates:
    print date
    print dated_forecast[date]
	

