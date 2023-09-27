#!/usr/bin/python2.7


def yr_forecast_data():
    # Weather forecast from yr.no, delivered by the Norwegian Meteorological Institute and the NRK
    import urllib
    # import datetime
    from datetime import datetime
    from xml.dom import minidom

    from forecast_db_interface import YrTable, forecast_db_interface, toFloat

    url = "http://www.yr.no/place/Norway/S%C3%B8r-Tr%C3%B8ndelag/Trondheim/Trondheim/forecast.xml"
    # TODO : also parse http://www.yr.no/place/Norway/S%C3%B8r-Tr%C3%B8ndelag/Trondheim/Trondheim/forecast_hour_by_hour.xml in addition to the above. hour by hour only gives forecast for next 24 hours, but that is more detailed than above URL.

    dom = minidom.parse(urllib.urlopen(url))
    forecast = dom.getElementsByTagName("forecast")[0]
    tabular_forecast = forecast.getElementsByTagName("tabular")[0]

    dbIf = forecast_db_interface()
    dbIf.createTables()

    raw_forecasts = []
    dated_forecast = {}
    dates = []

    for node in tabular_forecast.getElementsByTagName("time"):
        symbol = node.getElementsByTagName("symbol")[0]
        precip = node.getElementsByTagName("precipitation")[0]
        windDir = node.getElementsByTagName("windDirection")[0]
        windSpeed = node.getElementsByTagName("windSpeed")[0]
        temp = node.getElementsByTagName("temperature")[0]
        pressure = node.getElementsByTagName("pressure")[0]

        date, sep, fromTime = node.getAttribute("from").partition("T")
        toTime = node.getAttribute("to").partition("T")[2]

        raw_forecasts.append(
            {
                "date": date,
                #'from'          : fromTime,
                #'to'            : toTime,
                "symbol": symbol.getAttribute("name"),
                "precipitation": precip.getAttribute("value"),
                "wind_dir": windDir.getAttribute("deg"),
                "wind_speed": windSpeed.getAttribute("mps"),
                "temperature": temp.getAttribute("value"),
                "pressure": pressure.getAttribute("value"),
                "humidity": "",
            }
        )
        if date in dates:
            dated_forecast[date].append(
                {
                    #'from'          : fromTime,
                    #'to'            : toTime,
                    "symbol": symbol.getAttribute("name"),
                    "precipitation": precip.getAttribute("value"),
                    "wind_dir": windDir.getAttribute("deg"),
                    "wind_speed": windSpeed.getAttribute("mps"),
                    "temperature": temp.getAttribute("value"),
                    "pressure": pressure.getAttribute("value"),
                    "humidity": "",
                }
            )
        else:
            dates.append(date)
            dated_forecast[date] = []
            dated_forecast[date].append(
                {
                    #'from'          : fromTime,
                    #'to'            : toTime,
                    "symbol": symbol.getAttribute("name"),
                    "precipitation": precip.getAttribute("value"),
                    "wind_dir": windDir.getAttribute("deg"),
                    "wind_speed": windSpeed.getAttribute("mps"),
                    "temperature": temp.getAttribute("value"),
                    "pressure": pressure.getAttribute("value"),
                    "humidity": "",
                }
            )
    counter = 0
    for date in dates:
        temp_min = None
        temp_max = None
        for items in dated_forecast[date]:
            tmp_val = float(items["temperature"])
            if temp_min is None or temp_min > tmp_val:
                temp_min = tmp_val
            if temp_max is None or temp_max < tmp_val:
                temp_max = tmp_val

        ##        values =(datetime.date.today(), date, dated_forecast[date][0]['symbol'], dated_forecast[date][0]['wind_dir'], dated_forecast[date][0]['wind_speed'],
        ##                temp_min, temp_max, dated_forecast[date][0]['pressure'], dated_forecast[date][0]['precipitation'], dated_forecast[date][0]['humidity'])
        newYrEntry = YrTable(
            # accesssDate=datetime.date.today()
            forecastDate=datetime.strptime(date, "%Y-%m-%d").date(),
            symbol=dated_forecast[date][0]["symbol"],
            windDir=dated_forecast[date][0]["wind_dir"],
            windSpeed=toFloat(dated_forecast[date][0]["wind_speed"]),
            tempMin=toFloat(temp_min),
            tempMax=toFloat(temp_max),
            pressure=toFloat(dated_forecast[date][0]["pressure"]),
            precipitation=toFloat(dated_forecast[date][0]["precipitation"]),
            humidity=toFloat(dated_forecast[date][0]["humidity"]),
        )
        dbIf.insertRow(newTuple=newYrEntry)
        counter = counter + 1
        if counter >= YrTable.MAX_DAYS_TO_PREDICT:
            break


if __name__ == "__main__":
    yr_forecast_data()
