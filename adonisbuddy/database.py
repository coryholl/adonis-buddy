# Copyright (C) 2024 Cory Jon Hollingsworth
#
# This file is part of Adonis Buddy.
#
# Adonis Buddy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Adonis Buddy.  If not, see <https://www.gnu.org/licenses/>.
import datetime
import os
import sqlite3
from kivy.app import App
# local imports
import database_util

class Database:
    app_db = None
    metrics_db = None

    def __init__(self):
        """
        __init__
        args: self - self object
        purpose: initialize database object
        """
        if not os.path.exists('database'):
            os.makedirs('database')
        app_db_file = os.path.join('database', 'app.sqlite3')
        self.app_db = sqlite3.connect(app_db_file) if os.path.exists(app_db_file) else \
            self.create_app_database(app_db_file)
        metrics_db_file = os.path.join('database', 'metrics.sqlite3')
        self.metrics_db = sqlite3.connect(metrics_db_file) if os.path.exists(metrics_db_file) else \
            self.create_metrics_database(metrics_db_file)

    def __exit__(self):
        """
        __exit__
        args: self - self object
        purpose: close database upon application exit
        """
        self.app_db.commit()
        self.app_db.close()
        self.metrics_db.commit()
        self.metrics_db.close()

    def create_app_database(self, database_file_name):
        """
        create_app_database
        args: self - self object
            database_file_name - database file name
        purpose: create an fresh Adonis Buddy app database
        returns: open sqlite3 database object for the app database
        """
        conn = sqlite3.connect(database_file_name)
        curs = conn.cursor()
        database_util.create_config_table(curs)
        conn.commit()
        curs.close()
        return conn

    def create_measurements_table(self, curs):
        """
        create_measurements_table
        args: self - self object
            curs - open database cursor
        purpose: create measurements table for storage of future measurements
        """
        sql = """
            CREATE TABLE "measurements" (
	            "date"	TEXT NOT NULL,
	            "name"	TEXT NOT NULL,
	            "value"	REAL NOT NULL,
	            "unit_type"	TEXT NOT NULL,
	            "measure_method" TEXT,
	            "sort_key" REAL NOT NULL,
	            PRIMARY KEY("date","name","measure_method")
            );
        """
        curs.execute(sql)

    def create_metrics_database(self, database_file_name):
        """
        create_metrics_database
        args: self - self object
            database_file_name - database file name
        purpose: create an fresh Adonis Buddy metrics database
        returns: open sqlite3 database object for the app database
        """
        conn = sqlite3.connect(database_file_name)
        curs = conn.cursor()
        self.create_measurements_table(curs)
        conn.commit()
        curs.close()
        return conn

    def get_circumference_images(self):
        """
        get_circumference_images
        args: self - self object
        purpose: load circumference mapping database
        returns: dictionary of circumference images table
        """
        sql = 'SELECT * FROM circumference_images ORDER BY body_part_name'
        return database_util.basic_query(self.app_db, sql)

    def get_color_dates_by_year_month(self, year, month):
        """
        get_color_dates_by_year_month
        args: self - self object
            year - year to select
            month - month to select
        purpose: forward color selection to correct query for color highlighting
        """
        return self.get_measuerments_dates_by_year_month(year, month)

    def get_measurement(self, date, name, measurement_method=False):
        """
        get_measurement
        args: self - self object
            date - date string
            name - name of measurement
            measurement_method - optional measurement method
        purpose: retrieve measurement from database
        returns: list of data dictionaries of measurement
        """
        if measurement_method is False:
            return database_util.basic_query(self.metrics_db,
                'SELECT * FROM measurements WHERE date = ? AND name = ?', values=(date, name))
        elif measurement_method is None:
            return database_util.basic_query(self.metrics_db,
                'SELECT * FROM measurements WHERE date = ? AND name = ? AND measure_method IS NULL',
                values=(date, name))
        else:
            return database_util.basic_query(self.metrics_db,
                'SELECT * FROM measurements WHERE date = ? AND name = ? AND measure_method = ?',
                values=(date, name, measurement_method))

    def get_birth_date(self):
        """
        get_birth_date
        args: self - self object
        purpose: retrieve birthdate from database
        returns: ISO formated birth date string
        """
        return database_util.basic_query(self.metrics_db,
            "SELECT value FROM measurements WHERE name = 'birth date' ORDER BY date DESC LIMIT 1")

    def get_measurements(self):
        """
        get_measurements
        args: self - self object
        purpose: retrieve contents of measurement table
        returns: list of dictionaries of measurements
        """
        return database_util.basic_query(self.metrics_db,
            'SELECT * FROM measurements ORDER BY date DESC, sort_key ASC, name ASC')

    def get_measurements_by_date(self, date):
        """
        get_measurements_by_date
        args: self - self object
            date - date to query by
        purpose: retrieve measurements for a specific date
        return: list of dictionaries of measurements
        """
        return database_util.basic_query(self.metrics_db,
            'SELECT * FROM measurements WHERE date = ? ORDER BY sort_key ASC, name ASC', values=(date,))

    def get_measuerments_dates_by_year_month(self, year, month):
        """
        get_workout_dates_by_year_month
        args: self - self object
            year - year to match on
            month - month to match on
        purpose: return list of workout days for datepicker cosmetics
        returns: list of dictionaries of ISO format date strings
        """
        date_str = f'{year:04}-{month:02}-%'
        sql = 'SELECT DISTINCT date FROM measurements WHERE date LIKE ?'
        return database_util.basic_query(self.metrics_db, sql, values=(date_str,))

    def get_sound_files(self):
        """
        get_sound_files
        args: self - self object
        purpose: return sound file list
        """
        return []

    def store_measurement(self, name, value, unit_type, measure_method, sort_key):
        """
        store_circumference_measurement
        args: self - self object
            name - name of measurement
            value - value of measurement
            unit_type - type of unit measurement is in
            measure_method - method of measurement
            sort_key - sort key for grouping output
        purpose: store a measurement in database
        """
        date_str = datetime.date.today().isoformat()
        db_measurement = self.get_measurement(date_str, name)
        if db_measurement:
            sql = """
                UPDATE measurements
                SET value = ?,
                    unit_type = ?
                WHERE date = ? AND
                    name = ? AND
                    measure_method """
            if measure_method is None:
                sql += 'IS NULL'
                database_util.basic_edit(self.metrics_db, sql, (value, unit_type, date_str, name))
            else:
                sql += '= ?'
                database_util.basic_edit(self.metrics_db, sql, (value, unit_type, date_str, name, measure_method))
        else:
            sql = """
                INSERT INTO measurements
                (date, name, value, unit_type, measure_method, sort_key)
                VALUES(?, ?, ?, ?, ?, ?)
            """
            database_util.basic_edit(self.metrics_db, sql,
                                     (date_str, name, value, unit_type, measure_method, sort_key))
        app = App.get_running_app()
        app.app_data_dict['unpickleable']['history'].update_today_label()
