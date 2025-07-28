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
from collections import OrderedDict
from kivy.app import App
from kivy.clock import Clock
from kivy.logger import Logger
from kivy.properties import StringProperty
from kivymd.uix.boxlayout import MDBoxLayout
# local imports
import over_press
import soft_keyboard
from text_input_util import TextInputUtil
from image_touch_util import ImageTouchUtil

class Calipers(MDBoxLayout, TextInputUtil, ImageTouchUtil):
    all_input_fields = OrderedDict()
    percentage = StringProperty('0.0%')
    screen_name = 'calipers'

    def __init__(self, **kwargs):
        """
        __init__
        args: self - self object
            kwargs - kivy arguments
        purpose: initialize the caliper recorder
        """
        super(MDBoxLayout, self).__init__(**kwargs)
        self.all_input_fields['chest_field_id'] = self.ids['chest_field_id']
        self.all_input_fields['waist_field_id'] = self.ids['waist_field_id']
        self.all_input_fields['thigh_field_id'] = self.ids['thigh_field_id']
        self.keyboard_button = soft_keyboard.render_keyboard_shortcut(self)

    def calculate_bf(self, skinfold1, skinfold2, skinfold3):
        """
        calculate_bf
        args: self - self object
            skinfold1 - first skinfold measurement in mm
            skinfold2 - second skinfold measurement in mm
            skinfold3 - third skinfold measurement in mm
        purpose calculate the BF percentage from measurements
        returns: body fat percentage using the Jackson/Pollock 3 measure formula
        """
        app = App.get_running_app()
        if app.app_data_dict['global properties']['birth date'] == 'NOT SET':
            bf = 0.0
        else:
            today = datetime.date.today()
            born = datetime.date.fromisoformat(app.app_data_dict['global properties']['birth date'])
            age = (today - born) / datetime.timedelta(days=365.2425)
            skinfolds = skinfold1 + skinfold2 + skinfold3
            density = 1.10938 - (0.0008267 * skinfolds) + (0.0000016 * (skinfolds ** 2)) - (0.0002574 * age)
            bf = (495 / density) - 450
        return bf

    def caliper_field_update(self, field_key, *kwargs): # called from kv file
        """
        caliper_field_update
        args: self - self object
            field_key - key of incoming field
            kwargs - additional possible kivy args
        purpose:
        """
        skinfolds = [float(field.text or 0) for field in self.all_input_fields.values()]
        bf = self.calculate_bf(*skinfolds)
        self.percentage = f'{bf:.1f}%'
        self.ids['save_calipers_id'].disabled = bool(self.percentage == '0.0%')

    def save_caliper_data(self): # called from kv file
        """
        save_caliper_data
        args: self - self object
        purpose: write measurements and BF% to database
        """
        app = App.get_running_app()
        if over_press.protect(app=app, vibrate=True):
            unpickleable = app.app_data_dict['unpickleable']
            stored_bf = unpickleable['database'].get_measurement(datetime.date.today().isoformat(), 'body fat',
                measurement_method='calipers')
            if stored_bf:
                unpickleable['confirmation popup'].open_confirm_popup('Replace body fat measurement?',
                    self.store_caliper_data, over_press_protected=True)
            else:
                self.store_caliper_data()

    def select_image(self, name): #called from kv file
        """
        select_image
        args: self - self object
            name - name of muscle
        purpose: set form for selected image
        """
        Logger.info(f'calipers: select_image {name}')
        super().select_image(name)
        self.defocus_all()
        self.ids[f'{name}_field_id'].focus = True

    def set_focus(self, input_field, *kwargs): # called from kv file
        """
        set_focus
        args: self - self object
            input_field - text input field object
            kwargs - additional possible kivy args
        purpose: set the ID of the field that was last in focus so focus can be restored
        returns: boolean indicator as to if over_press protection allowed execution
        """
        Logger.info(f'calipers: set_focus')
        ret_flag = super().set_focus(input_field, *kwargs)
        app = App.get_running_app()
        image_map = app.app_data_dict['unpickleable']['image map']
        found = False
        for key, field in self.all_input_fields.items():
            if field.focus:
                self.ids['select_image_id'].source = \
                    os.path.join('images', image_map[key.split('_', 1)[0]][self.screen_name]['display image file'])
                found = True
                break
        if not found:
            self.ids['select_image_id'].source = os.path.join('images', 'caliper-model.png')
        return ret_flag

    def store_caliper_data(self, *kwargs):
        """
        store_caliper_data
        args: self - self object
            kwargs - kivy arguments which contains button widget if called from popup
        purpose: write calipers measurements and body fat percentage to database
        """
        app = App.get_running_app()
        app.app_data_dict['unpickleable']['confirmation popup'].dismiss()
        db = app.app_data_dict['unpickleable']['database']
        skinfold1 = float(self.ids['chest_field_id'].text or 0)
        db.store_measurement('chest pinch', skinfold1, 'mm', 'calipers', 2.0)
        skinfold2 = float(self.ids['waist_field_id'].text or 0)
        db.store_measurement('waist pinch', skinfold2, 'mm', 'calipers', 2.1)
        skinfold3 = float(self.ids['thigh_field_id'].text or 0)
        db.store_measurement('thigh pinch', skinfold3, 'mm', 'calipers', 2.3)
        bf = self.calculate_bf(skinfold1, skinfold2, skinfold3)
        db.store_measurement('body fat', bf, 'percent', 'calipers', 2.4)
