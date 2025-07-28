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
from kivy.app import App
from kivymd.uix.boxlayout import MDBoxLayout
# local imports
import over_press
import soft_keyboard
from image_touch_util import ImageTouchUtil
from text_input_util import TextInputUtil

class BodyMeasurements(MDBoxLayout, TextInputUtil, ImageTouchUtil):
    all_input_fields = {}
    keyboard_button = None
    screen_name = 'circumference'

    def __init__(self, **kwargs):
        """
        __init__
        args: self - self object
            kwargs - kivy arguments
        purpose: do some initialization for selector
        """
        super(MDBoxLayout, self).__init__(**kwargs)
        self.all_input_fields['measurement field'] = self.ids['measurement_field_id']
        self.keyboard_button = soft_keyboard.render_keyboard_shortcut(self)

    def measurement_field_update(self):
        """
        measurement_field_update
        args: self - self object
        purpose: handle input for field
        """
        self.ids['save_measurement_button_id'].disabled = False if self.ids['measurement_field_id'].text else True

    def next_previous_measurement_button_press(self, direction):
        """
        next_previous_measurement_button_press
        args: self - self object
        purpose: go to next body circumference measurement
        """
        app = App.get_running_app()
        if over_press.protect(app=app, vibrate=True):
            image_map = app.app_data_dict['unpickleable']['image map']
            if self.ids['measurement_field_id'].hint_text == 'NO SELECTION':
                self.select_image('chest')
            else:
                image_list = list(image_map)
                name = self.ids['measurement_field_id'].hint_text
                next_name = 'thigh'
                while next_name == 'thigh':
                    index = image_list.index(name)
                    new_index = ((index + 1) % len(image_list) if direction == 'next' else (index - 1) if index else
                        len(image_list) - 1)
                    image_map[name]['selected'] = False
                    name = next_name = image_list[new_index]
                image_map[next_name]['selected'] = True
                self.select_image(next_name)

    def save_measurement_button_press(self):
        """
        save_measurement_button_press
        args: self - self object
        purpose: save the measurement to database
        """
        app = App.get_running_app()
        if over_press.protect(app=app, vibrate=True):
            field = self.ids['measurement_field_id']
            name = field.hint_text
            value = float(field.text) if field.text else False
            unit_type = 'cm' if self.ids['unit_select_button_id'].icon == 'alpha-c-circle' else 'in'
            if name != 'NO SELECTION' and value:
                app.app_data_dict['unpickleable']['database'].store_measurement(name, value, unit_type, None, 1.0)

    def select_image(self, name):
        """
        select_image
        args: self - self object
            name - name of muscle
        purpose: set form for selected image
        """
        super().select_image(name)
        self.ids['measurement_field_id'].hint_text = name

    def set_focus(self, input_field, *kwargs):
        """
        set_focus
        args: self - self object
            input_field - text input field object
            kwargs - unknown arguments
        purpose: set the ID of the field that was last in focus so focus can be restored
        returns: boolean indicator as to if over_press protection allowed execution
        """
        retval = super().set_focus(input_field, *kwargs)
        if self.ids['measurement_field_id'].hint_text == 'NO SELECTION':
            self.select_image('chest')
        return retval

    def unit_select_button_press(self):
        """
        unit_select_button_press
        args: self - self object
        purpose: process unit selection button press
        """
        if over_press.protect(vibrate=True):
            self.ids['unit_select_button_id'].icon = ('alpha-i-circle' if
                self.ids['unit_select_button_id'].icon == 'alpha-c-circle' else 'alpha-c-circle')
