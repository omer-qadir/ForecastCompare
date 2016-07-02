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


client = SoapClient(location="http://eklima.met.no/metdata/MetDataService")
response = client._url_to_xml_tree ("http://eklima.met.no/metdata/MetDataService?invoke=getMetData&timeserietypeID=0&format=&from=&to=&stations=68860&elements=UM%2CPRM%2CRR%2CTAMRR%2CFFM%2CTAN%2CTAX%2CDD18%2CNNM&hours=&months=&username=", False, False)
#print (response)
#repr(response)

weatherElement = response.__contains__ ('weatherElement')

#db = forecast_db_interface('WeatherForecast.db')
#db.create_table("VOLL")

raw_observations = []
dated_observations = {}
dates = []

for node in weatherElement.getElementsByTagName('item'):
    symbol      = []
    precip      = []
    windDir     = []
    windSpeed   = []
    temp        = []
    pressure    = []
    humidity    = []
    # date = node.getAttribute('day')
    currentId   = node.getElementsByTagName('id')

    #print (currentId)
    
#    raw_observations.append({
#        'date'          : date,
#        'from'          : '',
#        'to'            : '',
#        'symbol'        : symbol.getAttribute('name'),
#        'precipitation' : precip.getAttribute('value'),
#        'wind_dir'      : windDir.getAttribute('deg'),
#        'wind_speed'    : windSpeed.getAttribute('mps'),
#        'temperature'   : '',
#        'temp_min'      : temp.getAttribute('min'),
#        'temp_max'      : temp.getAttribute('max'),
#        'pressure'      : pressure.getAttribute('value'),
#        'humidity'      : humidity.getAttribute('value')
#    })
#    if date in dates:
#        dated_observations[date].append({
#            'from'          : '',
#            'to'            : '',
#            'symbol'        : symbol.getAttribute('name'),
#            'precipitation' : precip.getAttribute('value'),
#            'wind_dir'      : windDir.getAttribute('deg'),
#            'wind_speed'    : windSpeed.getAttribute('mps'),
#            'temperature'   : '',
#            'temp_min'      : temp.getAttribute('min'),
#            'temp_max'      : temp.getAttribute('max'),
#            'pressure'      : pressure.getAttribute('value'),
#            'humidity'      : humidity.getAttribute('value')
#        })
#    else:
#        dates.append(date)
#        dated_observations[date] = []
#        dated_observations[date].append({
#            'from'          : '',
#            'to'            : '',
#            'symbol'        : symbol.getAttribute('name'),
#            'precipitation' : precip.getAttribute('value'),
#            'wind_dir'      : windDir.getAttribute('deg'),
#            'wind_speed'    : windSpeed.getAttribute('mps'),
#            'temperature'   : '',
#            'temp_min'      : temp.getAttribute('min'),
#            'temp_max'      : temp.getAttribute('max'),
#            'pressure'      : pressure.getAttribute('value'),
#            'humidity'      : humidity.getAttribute('value')
#        })

# for date in dates:
    # print (date)
    # print (dated_observations[date])

#counter = 0
#for date in dates: 
#    values =(datetime.date.today(), date, dated_observations[date][0]['symbol'], dated_observations[date][0]['wind_dir'], dated_observations[date][0]['wind_speed'], 
#            dated_observations[date][0]['temp_min'], dated_observations[date][0]['temp_max'], dated_observations[date][0]['pressure'], 
#            dated_observations[date][0]['precipitation'], dated_observations[date][0]['humidity'])
#    db.insert_row("OWM",values)
#    counter = counter + 1
#    if counter >= forecast_db_interface.MAX_DAYS_TO_PREDICT:
#        break
#
#db.commit()
#db.close()


