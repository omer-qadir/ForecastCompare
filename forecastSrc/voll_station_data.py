#!/usr/bin/python2.7

def voll_station_data():
    #Weather forecast from open weather map
    import datetime
    #from datetime import datetime
    from forecast_db_interface import forecast_db_interface, VollTable, toFloat, db
    # https://github.com/pysimplesoap/pysimplesoap
    from pysimplesoap.client import SoapClient

    # http://eklima.met.no/wsKlima/start/start_en.html
    # http://eklima.met.no/metdata/MetDataService?operation=getMetData
    # http://eklima.met.no/eklimapub/servlet/ReportInfo?action=stationinfo&s=68860&la=en&co=US
    # http://sharki.oslo.dnmi.no/eklimapub/servlet/ReportInfo?action=parameterinfo&tab=T_ELEM_OBS&s=68860&la=en&co=US
    # http://eklima.met.no/Help/Stations/toDay/all/en_e68860.html

    # legend for values in XML : http://eklima.met.no/metdata/MetDataService?invoke=getElementsFromTimeserieTypeStation&timeserietypeID=0&stnr=68860
    lutObservedVals = {
            'humidity'       : []
           ,'pressure'       : []
           ,'precip'         : []
           ,'average_temp'   : []
           ,'windSpeed'      : []
           ,'temp_min'       : []
           ,'temp_max'       : []
           ,'windDir'        : []
           ,'symbol'         : []
          }
    lutMetElements = {
            'UM'    : 'humidity'
           ,'PRM'   : 'pressure'
           ,'RR'    : 'precip'
           ,'TAMRR' : 'average_temp'
           ,'FFM'   : 'windSpeed'
           ,'TAN'   : 'temp_min'
           ,'TAX'   : 'temp_max'
           ,'DD18'  : 'windDir'
           ,'NNM'   : 'symbol'
          }
    lutCloudCover = {
            0   : 'Clear Sky'
           ,1   : 'Mostly Sunny'
           ,2   : 'Partly Cloudy'
           ,3   : 'Cloudy'
           ,4   : 'Overcast'
           ,5   : 'Light rain'
           ,6   : 'Rain'
           ,7   : 'Heavy rain'
           ,-3  : 'Unknown'
          }



    client = SoapClient(location="http://eklima.met.no/metdata/MetDataService")
    #response = client._url_to_xml_tree ("http://tinyurl.com/hdpz55x", False, False)
    response = client._url_to_xml_tree ("http://eklima.met.no/metdata/MetDataService?invoke=getMetData&timeserietypeID=0&format=&from=&to=&stations=68860&elements=UM%2CPRM%2CRR%2CTAMRR%2CFFM%2CTAN%2CTAX%2CDD18%2CNNM&hours=&months=&username=", False, False)

    weatherElement = response.__contains__ ('weatherElement')

    dbIf = forecast_db_interface()
    dbIf.createTables()

    # print ("lutObservedVals" + str(lutObservedVals))
    # print ("lutMetElements" + str(lutMetElements))

    for node in weatherElement[0].getElementsByTagName('item'):
        currentId   = node.getElementsByTagName('id')[0].firstChild.data
        lutObservedVals[lutMetElements[currentId]] = node.getElementsByTagName('value')[0].firstChild.data

        #print (currentId + "=>" + lutObservedVals[lutMetElements[currentId]])

    #print (lutObservedVals)
    #print (lutObservedVals['symbol'])
    #print (float (lutObservedVals['symbol']) )
    #print (int(float (lutObservedVals['symbol']) ))
    #print (lutCloudCover.get(int(float (lutObservedVals['symbol']) ), 'Unknown'))



    newVollEntry =VollTable (
                             #accesssDate=datetime.date.today()
                             #forecastDate=datetime.strptime(date, '%Y-%m-%d').date()
                             forecastDate=datetime.date.today() #+ datetime.timedelta(days=10)
                            ,symbol= lutCloudCover.get(int(float (lutObservedVals['symbol']) ), 'Unknown')
                            ,windDir= lutObservedVals['windDir']
                            ,windSpeed=toFloat(lutObservedVals['windSpeed'])
                            ,tempMin=toFloat(lutObservedVals['temp_min'])
                            ,tempMax=toFloat(lutObservedVals['temp_max'])
                            ,pressure=toFloat(lutObservedVals['pressure'])
                            ,precipitation=toFloat(lutObservedVals['precip'])
                            ,humidity=toFloat(lutObservedVals['humidity'])
                          )
    #db.insert_row("VOLL",tupleValues)
    db.session.add(newVollEntry)

    db.session.commit()
    #db.close()


if __name__ == "__main__":
    voll_station_data()
