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
from kivy.utils import platform
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
# local imports
import soft_keyboard
from mb_config import Config as MBConfig

class Config(MBConfig):

    def __init__(self, **kwargs):
        """
        __init__
        args: self - self object
            kwargs - MDBoxLayout arguments
        purpose: initialize values on config page
        """
        super(MDBoxLayout, self).__init__(**kwargs)
        app = App.get_running_app()
        app.app_data_dict['unpickleable']['vibrate toggle method'] = self.toggle_vibrate
        config = app.app_data_dict['config']
        if platform == 'linux':
            app.app_data_dict['unpickleable']['hardware keyboard toggle method'] = self.toggle_hardware_keyboard
            self.enable_button('hardware keyboard')
        self.set_config_gui(config['software keyboard']['active'], 'software keyboard', app=app)

    def disable_soft_keyboard(self):
        """
        disable_soft_keyboard
        args: self - self object
        purpose: disable software keyboard throughout application
        """
        app = App.get_running_app()
        soft_keyboard.remove_soft_keyboard()
        unpickleable = app.app_data_dict['unpickleable']
        for key in ('body measurements', 'calipers', 'composition'):
            unpickleable[key].ids['keypad_button_container_id'].clear_widgets()

    def enable_soft_keyboard(self):
        """
        enable_soft_keyboard
        args: self - self object
        purpose: enable software keyboard through application
        """
        app = App.get_running_app()
        unpickleable = app.app_data_dict['unpickleable']
        size = app.app_data_dict['window height'] // 19
        for key in ('body measurements', 'calipers', 'composition'):
            button = MDIconButton(icon='keyboard-outline', icon_size=size)
            unpickleable[key].ids['keypad_button_container_id'].add_widget(button)
            button.bind(on_release=unpickleable[key].summon_keyboard_press)
