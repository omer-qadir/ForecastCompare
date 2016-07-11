#!/usr/bin/python2.7
## 
## import sqlite3
## import os.path
## 
## class forecast_db_interface:
##     MAX_DAYS_TO_PREDICT = 3
##     def __init__(self, db_name):
##         self.conn = sqlite3.connect(db_name)
##         self.conn = MySQLdb.connect (
##                                       host='omer.mysql.pythonanywhere-services.com'
##                                      ,user='omer'
##                                      ,passwd='forecast123'
##                                      ,db='omer$default'
##                                     )
##         self.cursor = self.conn.cursor()
## 
##     def create_table(self, table_name):
##         #Create table of table_name (forecaster name)
##         #forecast_from timestamp, forecast_to timestamp,
##         self.cursor.execute("CREATE TABLE IF NOT EXISTS " + table_name + '''(access_date date, forecast_date date, symbol text, wind_dir text, 
##                             wind_speed real, temp_min real, temp_max real, pressure real, precipitation real,
##                             humidity real)''')
## 
##     def insert_row(self, table_name, values):
##         # Insert a row of data
##         self.cursor.execute("INSERT INTO " + table_name + " VALUES (?,?,?,?,?,?,?,?,?,?)", values)
## 
##     def commit(self):
##         # Save (commit) the changes
##         self.conn.commit()
## 
##     def close(self):
##         self.conn.close()
## 

#!/usr/bin/python2.7

#import sqlite3
#import os.path
import datetime
#import sqlalchemy
from sqlalchemy import create_engine, Column, Float, Integer, Text, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
#from flask_app import db

Base = declarative_base()

class ForecastTable ():
    id = Column('id', Integer, primary_key=True)
    accesssDate = Column('Access date', Date)
    forecastDate = Column('Forecast date', Date)
    symbol = Column('Cloud Cover', Text)
    wind_dir = Column('Wind direction', Text)
    wind_speed = Column('Wind speed', Float)
    temp_min = Column('Temp min', Float)
    temp_max = Column('Temp max', Float)
    pressure = Column('Pressure', Float)
    precipitation = Column('Precipitation', Float)
    humidity = Column('Humidity', Float)


class BbcTable (ForecastTable, Base):
    __tablename__ = "BBC"
    __table_args__ = {'extend_existing': True}

class OwmTable (ForecastTable, Base):
    __tablename__ = "OWM"
    __table_args__ = {'extend_existing': True}


class YrTable (ForecastTable, Base):
    __tablename__ = "YR"
    __table_args__ = {'extend_existing': True}

class VollTable (ForecastTable, Base):
    __tablename__ = "VOLL"
    __table_args__ = {'extend_existing': True}

class forecast_db_interface ():

    MAX_DAYS_TO_PREDICT = 3

#    databaseName = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
#                                                       username="omer",
#                                                       password="forecast123",
#                                                       hostname="omer.mysql.pythonanywhere-services.com",
#                                                       databasename="omer$default",
#                                                       )
    databaseName = "sqlite:///WeatherForecast.db"

    # Create an engine that stores data in the local directory's
    # ///WeatherForecast.db file.
    engine = create_engine(databaseName)

    def __init__(self):
        #self.conn = sqlite3.connect(db_name)
        #self.cursor = self.conn.cursor()

        # Bind the engine to the metadata of the Base class so that the
        # declaratives can be accessed through a DBSession instance
        Base.metadata.bind = self.engine
        DBSession = sessionmaker(bind=self.engine)
        # A DBSession() instance establishes all conversations with the database
        # and represents a "staging zone" for all the objects loaded into the
        # database session object. Any change made against the objects in the
        # session won't be persisted into the database until you call
        # session.commit(). If you're not happy about the changes, you can
        # revert all of them back to the last commit by calling
        # session.rollback()
        self.session = DBSession()

    def createTables (self):
        # Create all tables in the engine. This is equivalent to "Create Table"
        # statements in raw SQL.
        Base.metadata.create_all(self.engine)


    def create_table(self, table_name):
        self.createTables()
##         #Create table of table_name (forecaster name)
##         #forecast_from timestamp, forecast_to timestamp,
##         forecastTable = db.Table (
##         id = db.Column('id', db.Integer, primary_key=True)
## 
##         self.cursor.execute("CREATE TABLE IF NOT EXISTS " + table_name + '''(access_date date, forecast_date date, symbol text, wind_dir text,
##                             wind_speed real, temp_min real, temp_max real, pressure real, precipitation real,
##                             humidity real)''')
##
##     def insert_row(self, table_name, values):
##         # Insert a row of data
##         self.cursor.execute("INSERT INTO " + table_name + " VALUES (?,?,?,?,?,?,?,?,?,?)", values)
## 
    def commit(self):
        # Save (commit) the changes
        self.session.commit()

    def close(self):
        self.session.close()


