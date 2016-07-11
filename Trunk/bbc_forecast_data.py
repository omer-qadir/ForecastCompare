#!/usr/bin/python2.7

# -*- coding: utf-8 -*-
def bbc_forecast_data():
    #Using weather forecast provided by BBC.
    import urllib
    import datetime
    from xml.dom import minidom
    from forecast_db_interface import forecast_db_interface, BbcTable, toFloat
    
    #url = 'http://tinyurl.com/bbc3dayforecast'
    url = 'http://open.live.bbc.co.uk/weather/feeds/en/3133880/3dayforecast.rss'
    
    dom = minidom.parse(urllib.urlopen(url))
    forecast = dom.getElementsByTagName('channel')[0]
    #db = forecast_db_interface('WeatherForecast.db')
    db = forecast_db_interface()
    db.create_table("BBC")
    
    raw_forecasts = []
    dated_forecast = {}
    
    
    daysOfWeek   = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
    monthsOfYear = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    
    startDateText           = forecast.getElementsByTagName('pubDate')[0].toxml()[9:25]
    startDay,startDateText  = startDateText.split(',')
    startDateText           = startDateText.lstrip()
    dy,mon,yr               = startDateText.split(' ')
    
    dates = []
    dates.append(datetime.date(int(yr),monthsOfYear.index(mon[0:3])+1,int(dy)))
    dates.append(dates[0] + datetime.timedelta(days=1))
    dates.append(dates[1] + datetime.timedelta(days=1))
    
    for node in forecast.getElementsByTagName('item'):
        title       = node.getElementsByTagName('title')[0]
        desc        = node.getElementsByTagName('description')[0]
        titleInfo   = title.toxml()[7:97].split(',')
        descInfo    = desc.toxml()[13:238].split(',')
    
        symbol      = titleInfo[0].split(':')[1].lstrip()
        maxIndex = -1
        maxTemp = ''
        if descInfo[0].split(':')[0] == 'Maximum Temperature':
            maxIndex = 0
            try:
                maxTemp     = int(descInfo[0].split(':')[1].lstrip()[0:3])
            except ValueError:
                try:
                    maxTemp     = int(descInfo[0].split(':')[1].lstrip()[0:2])
                except ValueError:
                    maxTemp     = int(descInfo[0].split(':')[1].lstrip()[0:1])
    
        minIndex = 1+maxIndex
        try:
            minTemp     = int(descInfo[minIndex].split(':')[1].lstrip()[0:3])
        except ValueError:
            try:
                minTemp     = int(descInfo[minIndex].split(':')[1].lstrip()[0:2])
            except ValueError:
                minTemp     = int(descInfo[minIndex].split(':')[1].lstrip()[0:1])
    
        #maxTemp = str(maxTemp)
        #minTemp = str(minTemp)
    
        windDir     = descInfo[2+maxIndex].split(':')[1].lstrip()
        windSpeed   = "{:.1f}".format(int(descInfo[3+maxIndex].split(':')[1].lstrip().replace('mph','')) * 0.44704)
        pressure    = descInfo[5+maxIndex].split(':')[1].lstrip().replace('mb','')
        humidity    = descInfo[6+maxIndex].split(':')[1].lstrip().replace('%','')
    
        dayGiven = titleInfo[0][0:3]
        if dayGiven == startDay:
            date = dates[0]
        elif dayGiven == daysOfWeek[(daysOfWeek.index(startDay) + 1)%7]:
            date = dates[1]
        else:
            date = dates[2]
        raw_forecasts.append({
            'date'          : date,
            'from'          : '',
            'to'            : '',
            'symbol'        : symbol,
            'precipitation' : '',
            'wind_dir'      : windDir,
            'wind_speed'    : windSpeed,
            'temperature'   : '',
            'temp_min'      : minTemp,
            'temp_max'      : maxTemp,
            'pressure'      : pressure,
            'humidity'      : humidity
        })
        if date in dated_forecast.keys():
            dated_forecast[date].append({
                'from'          : '',
                'to'            : '',
                'symbol'        : symbol,
                'precipitation' : '',
                'wind_dir'      : windDir,
                'wind_speed'    : windSpeed,
                'temperature'   : '',
                'temp_min'      : minTemp,
                'temp_max'      : maxTemp,
                'pressure'      : pressure,
                'humidity'      : humidity
            })
        else:
            dated_forecast[date] = []
            dated_forecast[date].append({
                'from'          : '',
                'to'            : '',
                'symbol'        : symbol,
                'precipitation' : '',
                'wind_dir'      : windDir,
                'wind_speed'    : windSpeed,
                'temperature'   : '',
                'temp_min'      : minTemp,
                'temp_max'      : maxTemp,
                'pressure'      : pressure,
                'humidity'      : humidity
    		})
    counter = 0
    for date in dates:
##        values =(datetime.date.today(), date, dated_forecast[date][0]['symbol'], dated_forecast[date][0]['wind_dir'], dated_forecast[date][0]['wind_speed'],
##                dated_forecast[date][0]['temp_min'], dated_forecast[date][0]['temp_max'], dated_forecast[date][0]['pressure'],
##                dated_forecast[date][0]['precipitation'], dated_forecast[date][0]['humidity'])
        #print (date)
        #print (type(date))
        newBbcEntry =BbcTable (
                                 #accesssDate=datetime.date.today()
                                 forecastDate=date
                                ,symbol=dated_forecast[date][0]['symbol']
                                ,windDir=dated_forecast[date][0]['wind_dir']
                                ,windSpeed=toFloat(dated_forecast[date][0]['wind_speed'])
                                ,tempMin=toFloat(dated_forecast[date][0]['temp_min'])
                                ,tempMax=toFloat(dated_forecast[date][0]['temp_max'])
                                ,pressure=toFloat(dated_forecast[date][0]['pressure'])
                                ,precipitation=toFloat(dated_forecast[date][0]['precipitation'])
                                ,humidity=toFloat(dated_forecast[date][0]['humidity'])
                              )
        #db.insert_row("BBC",values)
        db.session.add(newBbcEntry)
        counter = counter + 1
        if counter >= forecast_db_interface.MAX_DAYS_TO_PREDICT:
            break
    
    db.commit()
    db.close()
    
