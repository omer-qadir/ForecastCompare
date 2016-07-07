#!/usr/bin/python2.7

#Weather forecast from open weather map
import datetime
from forecast_db_interface import forecast_db_interface
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
response = client._url_to_xml_tree ("http://eklima.met.no/metdata/MetDataService?invoke=getMetData&timeserietypeID=0&format=&from=&to=&stations=68860&elements=UM%2CPRM%2CRR%2CTAMRR%2CFFM%2CTAN%2CTAX%2CDD18%2CNNM&hours=&months=&username=", False, False)

weatherElement = response.__contains__ ('weatherElement')

db = forecast_db_interface('WeatherForecast.db')
db.create_table("VOLL")

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



tupleValues = (
                 datetime.date.today()
                ,datetime.date.today()
                ,lutCloudCover.get(int(float (lutObservedVals['symbol']) ), 'Unknown')
                ,lutObservedVals['windDir']
                ,lutObservedVals['windSpeed']
                ,lutObservedVals['temp_min']
                ,lutObservedVals['temp_max']
                ,lutObservedVals['pressure']
                ,lutObservedVals['precip']
                ,lutObservedVals['humidity']
              )
db.insert_row("VOLL",tupleValues)

db.commit()
db.close()


