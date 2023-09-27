#!/usr/bin/python2.7

import datetime

from sqlalchemy import (Column, Date, Float, Integer, Text, UniqueConstraint,
                        and_)

# from sqlalchemy import create_engine
# from sqlalchemy import ForeignKeyConstraint
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
from flask_app import db

# Base = declarative_base()


class ForecastTable:
    MAX_DAYS_TO_PREDICT = 3

    id = Column("id", type_=Integer, primary_key=True)
    accessDate = Column(
        "AccessDate", type_=Date, default=datetime.date.today, nullable=False
    )
    forecastDate = Column("ForecastDate", type_=Date, nullable=False)
    symbol = Column("CloudCover", type_=Text)
    windDir = Column("WindDirection", type_=Text)
    windSpeed = Column("WindSpeed", type_=Float)
    tempMin = Column("TempMin", type_=Float)
    tempMax = Column("TempMax", type_=Float)
    pressure = Column("Pressure", type_=Float)
    precipitation = Column("Precipitation", type_=Float)
    humidity = Column("Humidity", type_=Float)

    def __repr__(self):
        return (
            "(id='%s', accessDate='%s', forecastDate='%s, symbol='%s, windDir='%s, windSpeed='%s, tempMin='%s, tempMax='%s, pressure='%s, precipitation='%s, humidity='%s')"
            % (
                self.id,
                self.accessDate,
                self.forecastDate,
                self.symbol,
                self.windDir,
                self.windSpeed,
                self.tempMin,
                self.tempMax,
                self.pressure,
                self.precipitation,
                self.humidity,
            )
        )


def toFloat(stringToConvert):
    try:
        return float(stringToConvert)
    except ValueError:
        return None


class BbcTable(ForecastTable, db.Model):
    __tablename__ = "BBC"
    # __table_args__ = {'extend_existing': True}
    # __table_args__ = (UniqueConstraint('accesssDate', 'forecastDate', name='_uniqueDate'),)
    # __table_args__ = (
    #                    ForeignKeyConstraint(['AccessDate'], ['Voll.AccessDate']),
    #                 )


class OwmTable(ForecastTable, db.Model):
    __tablename__ = "OWM"
    # __table_args__ = {'extend_existing': True}
    # __table_args__ = (UniqueConstraint('accesssDate', 'forecastDate', name='_uniqueDate'),)
    # __table_args__ = (
    #                    ForeignKeyConstraint(['AccessDate'], ['Voll.AccessDate']),
    #                 )


class YrTable(ForecastTable, db.Model):
    __tablename__ = "Yr"
    # __table_args__ = {'extend_existing': True}
    # __table_args__ = (UniqueConstraint('accesssDate', 'forecastDate', name='_uniqueDate'),)
    # __table_args__ = (
    #                    ForeignKeyConstraint(['AccessDate'], ['Voll.AccessDate']),
    #                 )


class VollTable(ForecastTable, db.Model):
    __tablename__ = "Voll"
    # __table_args__ = {'extend_existing': True}
    # __table_args__ = (UniqueConstraint('accesssDate', 'forecastDate', name='_uniqueDate'),)
    __table_args__ = (
        UniqueConstraint("ForecastDate", name="_uniqueDate"),
        UniqueConstraint("AccessDate", name="_uniqueDate"),
    )


class forecast_db_interface:
    def createTables(self):
        """Create all tables described in DB"""
        db.create_all()
        db.session.commit()

    def insertRow(self, newTuple):
        """Insert a row of data
        newTuple can be any instance of BbcTable, VollTable, YrTable, OwmTable
        """
        db.session.add(newTuple)
        db.session.commit()

    def dayAwayTable(self, numDays=1):
        """returns a sql-alchemy Query variable.
        The query joins the forecast date from each of BbcTable, YrTable, OwmTable
        to the forecast date of VollTable, and then filters it for <numDays> number
        of days in the future that the forecast was made.
        """
        return (
            db.session.query(VollTable, BbcTable, YrTable, OwmTable)
            .filter(
                and_(
                    VollTable.forecastDate == BbcTable.forecastDate,
                    VollTable.forecastDate == YrTable.forecastDate,
                    VollTable.forecastDate == OwmTable.forecastDate,
                )
            )
            .filter(
                and_(
                    BbcTable.forecastDate == BbcTable.accessDate + numDays,
                    YrTable.forecastDate == YrTable.accessDate + numDays,
                    OwmTable.forecastDate == OwmTable.accessDate + numDays,
                )
            )
        )


## SQL Queries
## ===========
## select Voll.ForecastDate, Voll.TempMax as Observed, BBC.TempMax as BBC, Yr.TempMax as Yr, OWM.TempMax as 'Open Weather' from Voll left join BBC on Voll.ForecastDate = BBC.ForecastDate left join Yr on Voll.ForecastDate = Yr.ForecastDate  left join OWM on Voll.ForecastDate = OWM.ForecastDate;
## select Voll.ForecastDate, Voll.TempMax as Observed, BBC.TempMax as BBC, Yr.TempMax as Yr, OWM.TempMax as 'Open Weather' from Voll inner join BBC on Voll.ForecastDate = BBC.ForecastDate inner join Yr on Voll.ForecastDate = Yr.ForecastDate  inner join OWM on Voll.ForecastDate = OWM.ForecastDate;
## select Voll.ForecastDate, Voll.TempMin as Observed, BBC.TempMin as BBC, Yr.TempMin as Yr, OWM.TempMin as 'Open Weather' from Voll left join BBC on Voll.ForecastDate = BBC.ForecastDate left join Yr on Voll.ForecastDate = Yr.ForecastDate  left join OWM on Voll.ForecastDate = OWM.ForecastDate;
## select * from BBC where ForecastDate = DATE_ADD(AccessDate, interval 1 day);
## select Voll.TempMax as Observed, BBCsel.TempMax as BBC from (select * from BBC where ForecastDate = DATE_ADD(AccessDate, interval 1 day)) as BBCsel, Voll where Voll.ForecastDate=BBCsel.ForecastDate;
## select BBCsel.AccessDate, BBCsel.ForecastDate, Voll.TempMax as Observed, BBCsel.TempMax as BBC from (select * from BBC where ForecastDate = DATE_ADD(AccessDate, interval 1 day)) as BBCsel, Voll where Voll.ForecastDate=BBCsel.ForecastDate;

## SQL-Alchemy Queries
## ===================
## from forecastSrc.forecast_db_interface import *; db.session.query(VollTable).join(BbcTable, VollTable.forecastDate == BbcTable.forecastDate)
## from forecastSrc.forecast_db_interface import *; db.session.query(VollTable).join(BbcTable, VollTable.forecastDate == BbcTable.forecastDate).join(YrTable, VollTable.forecastDate == YrTable.forecastDate).all()
## from forecastSrc.forecast_db_interface import *; db.session.query(BbcTable).filter(BbcTable.forecastDate==BbcTable.accessDate+1).all()
## from forecastSrc.forecast_db_interface import *; db.session.query(VollTable).join(BbcTable, VollTable.forecastDate == BbcTable.forecastDate).filter(BbcTable.forecastDate==BbcTable.accessDate+1).all()
## from forecastSrc.forecast_db_interface import *; db.session.query(VollTable,BbcTable).join(BbcTable, VollTable.forecastDate == BbcTable.forecastDate).filter(BbcTable.forecastDate==BbcTable.accessDate+1).all()
## from forecastSrc.forecast_db_interface import *; db.session.query(BbcTable).filter(VollTable.forecastDate == BbcTable.forecastDate).all()
## from forecastSrc.forecast_db_interface import *; db.session.query(BbcTable).filter(VollTable.forecastDate == BbcTable.forecastDate).filter(BbcTable.forecastDate==BbcTable.accessDate+1).all()
## from forecastSrc.forecast_db_interface import *; dbInterface = forecast_db_interface()
## from forecastSrc.forecast_db_interface import *; db.session.query(BbcTable,VollTable).filter(BbcTable.forecastDate==BbcTable.accessDate+1).join(VollTable, VollTable.forecastDate == BbcTable.forecastDate).all()
## from forecastSrc.forecast_db_interface import *; db.session.query(BbcTable,VollTable, YrTable).filter( and_ (BbcTable.forecastDate==BbcTable.accessDate+1, YrTable.forecastDate==YrTable.accessDate+1 ) )
## from forecastSrc.forecast_db_interface import *; db.session.query(VollTable, BbcTable,YrTable).filter(and_(VollTable.forecastDate == BbcTable.forecastDate, VollTable.forecastDate==YrTable.forecastDate)).filter( and_ (BbcTable.forecastDate==BbcTable.accessDate+1, YrTable.forecastDate==YrTable.accessDate+1 ) )
## from forecastSrc.forecast_db_interface import *; db.session.query(BbcTable,VollTable, YrTable, OwmTable).filter( and_ (BbcTable.forecastDate==BbcTable.accessDate+1, YrTable.forecastDate==YrTable.accessDate+1, OwmTable.forecastDate==OwmTable.accessDate+1 ) )
## from forecastSrc.forecast_db_interface import *; db.session.query(VollTable, BbcTable, YrTable, OwmTable).filter(and_(VollTable.forecastDate == BbcTable.forecastDate, VollTable.forecastDate==YrTable.forecastDate, VollTable.forecastDate==OwmTable.forecastDate))
## from forecastSrc.forecast_db_interface import *; db.session.query(VollTable, BbcTable, YrTable, OwmTable).filter(and_(VollTable.forecastDate == BbcTable.forecastDate, VollTable.forecastDate==YrTable.forecastDate, VollTable.forecastDate==OwmTable.forecastDate)).filter( and_ (BbcTable.forecastDate==BbcTable.accessDate+1, YrTable.forecastDate==YrTable.accessDate+1, OwmTable.forecastDate==OwmTable.accessDate+1 ) )
## from forecastSrc.forecast_db_interface import *; dbIf = forecast_db_interface(); dbIf.createTables()
