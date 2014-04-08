#Weather forecast from yr.no, delivered by the Norwegian Meteorological Institute and the NRK
import urllib
from xml.dom import minidom

url = 'http://www.yr.no/place/Norway/S%C3%B8r-Tr%C3%B8ndelag/Trondheim/Trondheim/forecast.xml'

dom = minidom.parse(urllib.urlopen(url))
forecast = dom.getElementsByTagName('forecast')[0]
tabular_forecast = forecast.getElementsByTagName('tabular')[0]

raw_forecasts = []
dated_forecast = {}
dates = []

for node in tabular_forecast.getElementsByTagName('time'):
    symbol      = node.getElementsByTagName('symbol')[0]
    precip      = node.getElementsByTagName('precipitation')[0]
    windDir     = node.getElementsByTagName('windDirection')[0]
    windSpeed   = node.getElementsByTagName('windSpeed')[0]
    temp        = node.getElementsByTagName('temperature')[0]
    pressure    = node.getElementsByTagName('pressure')[0]
    
    date,sep,fromTime = node.getAttribute('from').partition('T')
    toTime   = node.getAttribute('to').partition('T')[2]
    
    raw_forecasts.append({
        'date'          : date,
        'from'          : fromTime,
        'to'            : toTime,
        'symbol'        : symbol.getAttribute('name'),
        'precipitation' : precip.getAttribute('value'),
        'wind_dir'      : windDir.getAttribute('deg'),
        'wind_speed'    : windSpeed.getAttribute('mps'),
        'temperature'   : temp.getAttribute('value'),
        'pressure'      : pressure.getAttribute('value'),
        'humidity'      : ''
    })
    if date in dates:
		dated_forecast[date].append({
			'from'          : fromTime,
			'to'            : toTime,
			'symbol'        : symbol.getAttribute('name'),
			'precipitation' : precip.getAttribute('value'),
			'wind_dir'      : windDir.getAttribute('deg'),
			'wind_speed'    : windSpeed.getAttribute('mps'),
			'temperature'   : temp.getAttribute('value'),
			'pressure'      : pressure.getAttribute('value'),
            'humidity'      : ''
		})
    else:
		dates.append(date)
        	dated_forecast[date] = []
		dated_forecast[date].append({
			'from'          : fromTime,
			'to'            : toTime,
			'symbol'        : symbol.getAttribute('name'),
			'precipitation' : precip.getAttribute('value'),
			'wind_dir'      : windDir.getAttribute('deg'),
			'wind_speed'    : windSpeed.getAttribute('mps'),
			'temperature'   : temp.getAttribute('value'),
			'pressure'      : pressure.getAttribute('value'),
            'humidity'      : ''
		})

for date in dates:
    print date
    print dated_forecast[date]
	

