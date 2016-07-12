#!/usr/bin/python2.7

from forecastSrc.bbc_forecast_data import bbc_forecast_data
from forecastSrc.owm_forecast_data import owm_forecast_data
from forecastSrc.voll_station_data import voll_station_data
from forecastSrc.yr_forecast_data import yr_forecast_data

bbc_forecast_data()
owm_forecast_data()
voll_station_data()
yr_forecast_data()
