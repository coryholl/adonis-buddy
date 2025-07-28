# Copyright (C) 2025 Cory Jon Hollingsworth
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
import kivy
import os
from kivy.base import stopTouchApp
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.utils import platform
from kivy.loader import Loader
from kivy.logger import Logger
from kivy.properties import BooleanProperty, StringProperty
from kivymd.app import MDApp
#local imports
import about
import android_util
import body_measurements
import calipers
import composition_measurements
import config
import database
import datadict
import linux_mobile_util
import measurement_history
import quit
import soft_keyboard
import sound
import vibrator
from confirmation_popup_window import ConfirmationPopupWindow
from date_picker import DatePicker
kivy.require('2.2.0')

class AdonisBuddyApp(MDApp):
    app_data_dict = {}
    load_disable = BooleanProperty(True)
    navigation_map = {
        'About': {
            'title': 'About',
            'screen': None
        },
        'Calipers': {
            'title': 'Body Fat Calipers',
            'screen': None
        },
        'Composition': {
            'title': 'Composition Measurements',
            'screen': None
        },
        'Config': {
            'title': 'Configure Features',
            'screen': None
        },
        'History': {
            'title': 'Measurements History',
            'screen': None
        },
        'Measurements': {
            'title': 'Body Measurements',
            'screen': None
        },
        'Quit': {
            'title': 'Quit',
            'screen': None
        }
    }
    title = StringProperty('Adonis Buddy')

    def __init__(self, data_dict):
        """
        __init__
        args: self - self object
            data_dict - data dictionary
        purpose:
        :param data_dict:
        """
        self.app_data_dict = data_dict
        super(AdonisBuddyApp, self).__init__()

    def build(self): # called from Kivy engine
        """
        build
        args: self - self object
        purpose: Kivy build method.  Builds and initializes the Kivy app.  Required for Kivy to run.
        """
        self.icon = Loader.loading_image = 'adonis_buddy.png'
        Logger.info('view: build: called')
        if platform == 'win':
            Window.fullscreen = True
        else:
            linux_mobile_util.set_mobile_fullscreen()
        if platform == 'android':
            Window.bind(on_keyboard=android_util.prevent_android_crash)
        self.shutdown_button_pressed_false = False
        self.reset_button_pressed_flag = False
        Loader.loading_image = 'adonis_buddy.png'
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_hue = "200"
        self.icon = 'adonis_buddy.png'
        if os.path.exists('no_load_sleep'):
            self.load_slow_resources(None)
        else:
            Clock.schedule_once(self.load_slow_resources, (4 if platform == 'android' else 2))

    def load_slow_resources(self, dt):
        """
        load_slow_resources
        args: self - self object
            dt - time since last callback call
        purpose: load slow loading resources
        """
        Logger.info('view: load_slow_resource')
        data_dict_obj = datadict.DataDict()
        data_dict_obj.get_data_dict(self.app_data_dict)
        soft_keyboard.init_keyboards()
        unpickleable = self.app_data_dict['unpickleable']
        unpickleable['about'] = self.navigation_map['About']['screen'] = about.About()
        unpickleable['birth date dialog'] = DatePicker(firstweekday=6, max_year=datetime.date.today().year+1,
            color_picker_func=lambda x, y: [])
        unpickleable['body measurements'] = self.navigation_map['Measurements']['screen'] = \
            body_measurements.BodyMeasurements()
        unpickleable['calipers'] = self.navigation_map['Calipers']['screen'] = calipers.Calipers()
        unpickleable['composition'] = self.navigation_map['Composition']['screen'] = \
            composition_measurements.CompositionMeasurements()
        unpickleable['config'] = self.navigation_map['Config']['screen'] = config.Config()
        unpickleable['confirmation popup'] = ConfirmationPopupWindow()
        unpickleable['history'] = self.navigation_map['History']['screen'] = measurement_history.MeasurementHistory()
        unpickleable['quit'] = self.navigation_map['Quit']['screen'] = quit.Quit()
        unpickleable['sound'] = sound.Sound(unpickleable['database'])
        unpickleable['vibrator'] = vibrator.Vibrator()
        linux_mobile_util.disable_squeekboard()
        self.root.ids['screen_container'].clear_widgets()
        self.root.ids['screen_container'].add_widget(self.navigation_map['Measurements']['screen'])
        self.title = self.navigation_map['Measurements']['title']
        self.load_disable = False

    def on_pause(self):
        """
        on_pause
        args: self - self object
        purpose: dump state when application is paused on Android
        returns: True
        """
        Logger.info('view: on_pause')
        return True

    def on_resume(self): # called from Kivy engine on Android
        """
        on_resume
        args: self - self object
        purpose: restore state after an Android pause
        """
        Logger.info('view: on_resume')

    def on_start(self): # called from Kivy engine on Android
        """
        on_start
        args: self - self object
        purpose: run any start logic
        """
        Logger.info('view: on_start')

    def on_stop(self, *kwargs):
        """
        on_stop
        args: self - self object
            *kwargs - optional arguments so it can be called from Clock
        purpose: shutdown app
        """
        Logger.info('view: on_stop')
        linux_mobile_util.enable_squeekboard()
        stopTouchApp()
