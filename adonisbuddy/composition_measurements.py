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
from workout_text_field import WorkoutTextField

class CompositionMeasurements(MDBoxLayout, TextInputUtil):
    all_input_fields = OrderedDict()
    dob_string = StringProperty('NOT SET')

    def __init__(self, **kwargs):
        """
        __init__
        args: self - self object
            kwargs - kivy arguments
        purpose: do some initialization for composition recorder form
        """
        super(MDBoxLayout, self).__init__(**kwargs)
        app = App.get_running_app()
        self.all_input_fields['height_foot_id'] = self.ids['height_foot_id']
        self.all_input_fields['height_inch_id'] = self.ids['height_inch_id']
        self.all_input_fields['height_cm_id'] = WorkoutTextField(field_name='height_cm_id',
            font_size=app.app_data_dict['window height'] // 30, hint_text='CM', input_field_type='int',
            input_filter='int', size_hint_x=0.8, disabled=True)
        self.all_input_fields['weight_id'] = self.ids['weight_id']
        self.all_input_fields['body_fat_measurement_id'] = self.ids['body_fat_measurement_id']
        self.all_input_fields['body_fat_measurement_type_id'] = self.ids['body_fat_measurement_type_id']
        self.all_input_fields['heart_rate_id'] = self.ids['heart_rate_id']
        print(app.app_data_dict['global properties']['birth date'])
        self.dob_string = app.app_data_dict['global properties']['birth date']
        self.keyboard_button = soft_keyboard.render_keyboard_shortcut(self)

    def check_body_fat_save(self, *kwargs):
        """
        check_body_fat_save
        args: self - self object
            kwargs - kivy arguments that contain button if called from popup
        purpose: check to see if we have body fat data to save
        """
        app = App.get_running_app()
        unpickleable = app.app_data_dict['unpickleable']
        unpickleable['confirmation popup'].dismiss()
        if self.ids['body_fat_measurement_id'].text:
            stored_bf = unpickleable['database'].get_measurement(datetime.date.today().isoformat(), 'body fat',
                measurement_method=(self.ids['body_fat_measurement_type_id'].text or None))
            if stored_bf:
                Clock.schedule_once(self.confirm_replace_body_fat, 0.5)
            else:
                self.store_body_fat()
        else:
            self.check_heart_save()

    def check_heart_save(self, *kwargs):
        """
        check_heart_save
        args: self - self object
            kwargs - kivy arguments that contain button if called from popup
        purpose: check to see if we have heart rate to save
        """
        app = App.get_running_app()
        unpickleable = app.app_data_dict['unpickleable']
        unpickleable['confirmation popup'].dismiss()
        if self.ids['heart_rate_id'].text:
            stored_heart_rate = unpickleable['database'].get_measurement(datetime.date.today().isoformat(),
                'heart rate')
            if stored_heart_rate:
                Clock.schedule_once(self.confirm_replace_heart, 0.5)
            else:
                self.store_heart_rate()

    def check_height_save(self, *kwargs):
        """
        check_height_save
        args: self - self object
            kwargs - kivy arguments that contain button if called from popup
        purpose: check to see if we have a height measurement to save
        """
        if ((self.all_input_fields['height_cm_id'].disabled and (self.all_input_fields['height_foot_id'].text or
                self.all_input_fields['height_inch_id'].text)) or (
                not self.all_input_fields['height_cm_id'].disabled and self.all_input_fields['height_cm_id'].text)):
            app = App.get_running_app()
            unpickleable = app.app_data_dict['unpickleable']
            stored_height = unpickleable['database'].get_measurement(datetime.date.today().isoformat(), 'height')
            if stored_height:
                Clock.schedule_once(self.confirm_replace_height, 0.5)
            else:
                self.store_height()
        else:
            self.check_weight_save()

    def check_weight_save(self, *kwargs):
        """
        check_weight_save
        args: self - self object
            kwargs - kivy arguments that contain button if called from popup
        purpose: check to see if we have a weight to save
        """
        app = App.get_running_app()
        unpickleable = app.app_data_dict['unpickleable']
        unpickleable['confirmation popup'].dismiss()
        if self.ids['weight_id'].text:
            stored_weight = unpickleable['database'].get_measurement(datetime.date.today().isoformat(), 'weight')
            if stored_weight:
                Clock.schedule_once(self.confirm_replace_weight, 0.5)
            else:
                self.store_weight()
        else:
            self.check_body_fat_save()

    def confirm_replace_body_fat(self, dt):
        """
        confirm_replace_body_fat
        args: self - self object
            dt - Kivy Clock time object
        purpose: open popup to confirm replacement of recorded body fat
        """
        app = App.get_running_app()
        app.app_data_dict['unpickleable']['confirmation popup'].open_confirm_popup(
            "Replace today's recorded body fat percentage?", self.store_body_fat,
            cancel_bind_method=self.check_heart_save)

    def confirm_replace_heart(self, dt):
        """
        confirm_replace_heart
        args: self - self object
            dt - Kivy Clock time object
        purpose: open popup to confirm replacement of recorded heart rate
        """
        app = App.get_running_app()
        app.app_data_dict['unpickleable']['confirmation popup'].open_confirm_popup(
            "Replace today's recorded heart rate?", self.store_heart_rate)

    def confirm_replace_height(self, dt):
        """
        confirm_replace_height
        args: self - self object
            dt - Kivy Clock time object
        purpose: open popup to confirm replacement of recorded height
        """
        app = App.get_running_app()
        app.app_data_dict['unpickleable']['confirmation popup'].open_confirm_popup("Replace today's recorded height?",
            self.store_height, cancel_bind_method=self.check_weight_save)

    def confirm_replace_weight(self, dt):
        """
        confirm_replace_weight
        args: self - self object
            dt - kivy Clock time object
        purpose: open popup to confirm replacement of recorded weight
        """
        app = App.get_running_app()
        app.app_data_dict['unpickleable']['confirmation popup'].open_confirm_popup("Replace today's recorded weight?",
            self.store_weight, cancel_bind_method=self.check_body_fat_save)

    def on_cancel(self, instance, value):
        """
        on_cancel
        args: self - self object
            instance - unused MDDatePicker object reference
            value - unused returned value
        purpose: binds to cancel button on date picker
        """
        Logger.info('composition_measurements: on_cancel')
        over_press.protect(vibrate=True)

    def on_save(self, instance, date, date_range):
        """
        on_save
        args: self - self object
            instance - unused MDDatePicker object reference
            date - selected date in datetime.date object
            date_range - empty date range
        purpose: display exercises performed on a specific date
        """
        Logger.info(f'composition_measurements: on_save {date}')
        if over_press.protect(vibrate=True):
            self.dob_string = date.isoformat()

    def save_metrics(self):
        """
        save_metrics
        args: self - self object
        purpose: write metrics to database
        """
        Logger.info(f'composition_measurements: save_metrics')
        app = App.get_running_app()
        if over_press.protect(app=app, vibrate=True):
            if self.dob_string in ('NOT SET', app.app_data_dict['global properties']['birth date']):
                self.check_height_save()
            else:
                app.app_data_dict['unpickleable']['confirmation popup'].open_confirm_popup(
                    'Replace birth date?', self.store_birth_date, over_press_protected=True,
                    cancel_bind_method=self.check_height_save)

    def select_birth_date(self):
        """
        select_birth_date
        args: self - self object
        purpose: select birthdate
        """
        app = App.get_running_app()
        if over_press.protect(app=app, vibrate=True):
            date_dialog = app.app_data_dict['unpickleable']['birth date dialog']
            date_dialog.title_input = 'Input Date'
            date_dialog.title = 'Select Date of Birth'
            date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
            date_dialog.open()

    def store_birth_date(self, *kwargs):
        """
        store_birth_date
        args: self - self object
            kwargs - kivy arguments which contains button widget if called from popup
        purpose: store birthdate to database
        """
        app = App.get_running_app()
        unpickleable = app.app_data_dict['unpickleable']
        unpickleable['confirmation popup'].dismiss()
        app.app_data_dict['global properties']['birth date'] = self.dob_string
        unpickleable['database'].store_measurement('birth date', self.dob_string, 'iso format date', None, 0)
        self.check_height_save()

    def store_body_fat(self, *kwargs):
        """
        store_body_fat
        args: self - self object
            kwargs - kivy arguments which contains button widget if called from popup
        purpose: extract body fat percent for storage to database
        """
        app = App.get_running_app()
        unpickleable = app.app_data_dict['unpickleable']
        unpickleable['confirmation popup'].dismiss()
        unpickleable['database'].store_measurement('body fat', float(self.ids['body_fat_measurement_id'].text),
            'percent', (self.ids['body_fat_measurement_type_id'].text or None), 3.3)
        self.check_heart_save()

    def store_heart_rate(self, *kwargs):
        """
        store_heart_rate
        args: self - self object
            kwargs - kivy arguments which contains button widget if called from popup
        purpose: extract heart rate for storage to database
        """
        app = App.get_running_app()
        unpickleable = app.app_data_dict['unpickleable']
        unpickleable['confirmation popup'].dismiss()
        unpickleable['database'].store_measurement('heart rate', float(self.ids['heart_rate_id'].text), 'bpm', None,
                                                   3.2)

    def store_height(self, *kwargs):
        """
        store_height
        args: self - self object
            kwargs - kivy arguments which contains button widget if called from popup
        purpose: extract the height for storage to database
        """
        app = App.get_running_app()
        unpickleable = app.app_data_dict['unpickleable']
        unpickleable['confirmation popup'].dismiss()
        db = unpickleable['database']
        if self.all_input_fields['height_cm_id'].disabled:
            inches = (float(self.all_input_fields['height_foot_id'].text) * 12.0 +
                float(self.all_input_fields['height_inch_id'].text))
            db.store_measurement('height', inches, 'in', None, 3.0)
        else:
            cm = float(self.all_input_fields['height_cm_id'].text)
            db.store_measurement('height', cm, 'cm', None, 3.0)
        self.check_weight_save()

    def store_weight(self, *kweargs):
        """
        store_weight
        args: self - self object
            kwargs - kivy arguements which contain button widget if called from popup
        purpose: extract weight and store to database
        """
        app = App.get_running_app()
        unpickleable = app.app_data_dict['unpickleable']
        unpickleable['confirmation popup'].dismiss()
        unpickleable['database'].store_measurement('weight', float(self.ids['weight_id'].text),
            self.ids['weight_unit_id'].text, None, 3.1)
        self.check_body_fat_save()

    def toggle_height_unit_button_press(self):
        """
        toggle_height_unit_button_press
        args: self - self object
        purpose: set form to display correct format for height measurements
        """
        if over_press.protect(vibrate=True):
            unit_button = self.ids['height_unit_id']
            inch_field = self.all_input_fields['height_inch_id']
            foot_field = self.all_input_fields['height_foot_id']
            cm_field = self.all_input_fields['height_cm_id']
            height_container = self.ids['height_container_id']
            if unit_button.text == 'cm':
                unit_button.icon = 'ruler'
                unit_button.text = 'in'
                cm_field.disabled = True
                height_container.remove_widget(cm_field)
                foot_field.disabled = inch_field.disabled = False
                height_container.add_widget(foot_field, index=1)
                height_container.add_widget(inch_field, index=1)
            else:
                unit_button.icon = 'tape-measure'
                unit_button.text = 'cm'
                foot_field.disabled = inch_field.disabled = True
                height_container.remove_widget(foot_field)
                height_container.remove_widget(inch_field)
                cm_field.disabled = False
                height_container.add_widget(cm_field, index=1)

    def toggle_weight_unit_button_press(self):
        """
        toggle_weight_unit_button_press
        args: self - self object
        purpose: set weight unit for weight insertion
        """
        if over_press.protect(vibrate=True):
            unit_button = self.ids['weight_unit_id']
            if unit_button.text == 'kg':
                unit_button.icon = 'weight-pound'
                unit_button.text = 'lbs'
            else:
                unit_button.icon = 'weight-kilogram'
                unit_button.text = 'kg'
