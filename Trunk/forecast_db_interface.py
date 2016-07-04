#!/usr/bin/python

import sqlite3
import os.path

class forecast_db_interface:
    MAX_DAYS_TO_PREDICT = 3
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_table(self, table_name):
        #Create table of table_name (forecaster name)
        #forecast_from timestamp, forecast_to timestamp,
        self.cursor.execute("CREATE TABLE IF NOT EXISTS " + table_name + '''(access_date date, forecast_date date, symbol text, wind_dir text, 
                            wind_speed real, temp_min real, temp_max real, pressure real, precipitation real,
                            humidity real)''')

    def insert_row(self, table_name, values):
        # Insert a row of data
        self.cursor.execute("INSERT INTO " + table_name + " VALUES (?,?,?,?,?,?,?,?,?,?)", values)

    def commit(self):
        # Save (commit) the changes
        self.conn.commit()

    def close(self):
        self.conn.close()
