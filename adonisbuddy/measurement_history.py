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
from kivy.app import App
from kivy.uix.label import Label
from kivymd.uix.boxlayout import MDBoxLayout

class MeasurementHistory(MDBoxLayout):

    def __init__(self):
        """
        __init__
        args: self - self object
        purpose: initialize measurement history
        """
        super().__init__()
        app = App.get_running_app()
        measurements = app.app_data_dict['unpickleable']['database'].get_measurements()
        date_str = ''
        label = None
        key = -1
        for measurement in measurements:
            if measurement['date'] != date_str:
                if label:
                    self.ids['measurements_carousel'].add_widget(label)
                date_str = measurement['date']
                label = Label(font_size=app.app_data_dict['window height'] // 30, markup=True)
                label.text = f'{date_str}\n'
            if measurement['name'] == 'birth date':
                continue
            if key != -1 and key != int(measurement['sort_key']):
                label.text += '\n'
            key = int(measurement['sort_key'])
            label.text += self.gen_label_row(measurement['name'], measurement['value'], measurement['unit_type'],
                    measurement['measure_method'])
        if label:
            self.ids['measurements_carousel'].add_widget(label)

    def update_today_label(self):
        """
        update_today_label
        args: self - self object
        purpose: generate label text for today's carousel label
        returns: string for label
        """
        app = App.get_running_app()
        today = datetime.date.today().isoformat()
        measurements = app.app_data_dict['unpickleable']['database'].get_measurements_by_date(today)
        if measurements:
            if (self.ids['measurements_carousel'].slides and
                    self.ids['measurements_carousel'].slides[0].text.startswith(today)):
                label = self.ids['measurements_carousel'].slides[0]
            else:
                label = Label(font_size=app.app_data_dict['window height'] // 30, markup=True)
                self.ids['measurements_carousel'].add_widget(label, index=-1)
            label.text = f'{today}\n'
            key = -1
            for measurement in measurements:
                if measurement['name'] == 'birth date':
                    continue
                if key != -1 and key != int(measurement['sort_key']):
                    label.text += '\n'
                key = int(measurement['sort_key'])
                label.text += self.gen_label_row(measurement['name'], measurement['value'], measurement['unit_type'],
                    measurement['measure_method'])

    def gen_label_row(self, name, value, unit_type, measure_method):
        """
        gen_label_row
        args: self - self object
            name - name of measurement
            value - value measured
            unit_type - unit measurement is stored
            measure_method - measurement method, may be None
        purpose: generate label line
        returns: string containing data
        """
        if name == 'body fat':
            value = f"{float(value):.1f}"
        elif name == 'height' and unit_type == 'in':
            height = float(value)
            foot = int(height // 12)
            inch = height % 12
            value = f'{foot}ft {inch}in'
            unit_type = ''
        else:
            value = f"{float(value)}"
        text = f"{name}: {value} {unit_type}"
        text += f" by {measure_method}\n" if measure_method else '\n'
        return text
