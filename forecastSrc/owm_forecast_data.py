#!/usr/bin/python2.7

def owm_forecast_data():

    #Weather forecast from open weather map
    import urllib
    #import datetime
    from datetime import datetime
    from xml.dom import minidom
    from forecast_db_interface import forecast_db_interface, OwmTable, toFloat, db

    url = 'http://api.openweathermap.org/data/2.5/forecast/daily?id=3133880&mode=xml&units=metric&appid=a3b3c3f0f20a5478a83f61aa4fd98505'

    dom = minidom.parse(urllib.urlopen(url))
    forecast = dom.getElementsByTagName('forecast')[0]

    dbIf = forecast_db_interface()
    dbIf.createTables()

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
        date        = node.getAttribute('day')

        raw_forecasts.append({
            'date'          : date,
            #'from'          : '',
            #'to'            : '',
            'symbol'        : symbol.getAttribute('name'),
            'precipitation' : precip.getAttribute('value'),
            'wind_dir'      : windDir.getAttribute('deg'),
            'wind_speed'    : windSpeed.getAttribute('mps'),
            #'temperature'   : '',
            'temp_min'      : temp.getAttribute('min'),
            'temp_max'      : temp.getAttribute('max'),
            'pressure'      : pressure.getAttribute('value'),
            'humidity'      : humidity.getAttribute('value')
        })
        if date in dates:
            dated_forecast[date].append({
                #'from'          : '',
                #'to'            : '',
                'symbol'        : symbol.getAttribute('name'),
                'precipitation' : precip.getAttribute('value'),
                'wind_dir'      : windDir.getAttribute('deg'),
                'wind_speed'    : windSpeed.getAttribute('mps'),
                #'temperature'   : '',
                'temp_min'      : temp.getAttribute('min'),
                'temp_max'      : temp.getAttribute('max'),
                'pressure'      : pressure.getAttribute('value'),
                'humidity'      : humidity.getAttribute('value')
            })
        else:
            dates.append(date)
            dated_forecast[date] = []
            dated_forecast[date].append({
                #'from'          : '',
                #'to'            : '',
                'symbol'        : symbol.getAttribute('name'),
                'precipitation' : precip.getAttribute('value'),
                'wind_dir'      : windDir.getAttribute('deg'),
                'wind_speed'    : windSpeed.getAttribute('mps'),
                #'temperature'   : '',
                'temp_min'      : temp.getAttribute('min'),
                'temp_max'      : temp.getAttribute('max'),
                'pressure'      : pressure.getAttribute('value'),
                'humidity'      : humidity.getAttribute('value')
            })

    # for date in dates:
        # print (date)
        # print (dated_forecast[date])

    counter = 0
    for date in dates:
##        values =(datetime.date.today(), date, dated_forecast[date][0]['symbol'], dated_forecast[date][0]['wind_dir'], dated_forecast[date][0]['wind_speed'],
##                dated_forecast[date][0]['temp_min'], dated_forecast[date][0]['temp_max'], dated_forecast[date][0]['pressure'],
##                dated_forecast[date][0]['precipitation'], dated_forecast[date][0]['humidity'])
        #print (date)
        #print (type(date))
        newOwmEntry =OwmTable (
                                 #accesssDate=datetime.date.today()
                                 forecastDate=datetime.strptime(date, '%Y-%m-%d').date()
                                ,symbol=dated_forecast[date][0]['symbol']
                                ,windDir=dated_forecast[date][0]['wind_dir']
                                ,windSpeed=toFloat(dated_forecast[date][0]['wind_speed'])
                                ,tempMin=toFloat(dated_forecast[date][0]['temp_min'])
                                ,tempMax=toFloat(dated_forecast[date][0]['temp_max'])
                                ,pressure=toFloat(dated_forecast[date][0]['pressure'])
                                ,precipitation=toFloat(dated_forecast[date][0]['precipitation'])
                                ,humidity=toFloat(dated_forecast[date][0]['humidity'])
                              )
        #db.insert_row("OWM",values)
        db.session.add(newOwmEntry)
        counter = counter + 1
        if counter >= OwmTable.MAX_DAYS_TO_PREDICT:
            break

    db.session.commit()
    #db.close()

if __name__ == "__main__":
    owm_forecast_data()
