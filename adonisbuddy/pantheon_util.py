# Copyright (C) 2025 Cory Jon Hollingsworth
#
# This file is part of the Pantheon suite.
#
# The Pantheon suite is free software: you can redistribute it and/or modify
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
# along with the Pantheon suite.  If not, see <https://www.gnu.org/licenses/>.
import os
from kivy.app import App
from kivy.base import stopTouchApp
from kivy.core.window import Window
from kivy.logger import Logger
from kivy.utils import platform
#local imports
import android_util
import over_press
from text_input_util import TextInputUtil

__version__ = '1.0.0'

def calibrate_screen(app_data_dict):
    """
    calibrate_screen
    args: app_data_dict - application's data dictionary
    purpose: establish screen dimensions
    """
    with open('scale.kv', 'r') as file:
       old_scale_text = file.read()
    app_data_dict['window height'] = Window.height
    app_data_dict['window width'] = Window.width
    new_scale_text = '#:set window_width {}\n#:set window_height {}\n'.format(Window.width, Window.height)
    if new_scale_text != old_scale_text:
        with open('scale.kv', 'w') as file:
           file.write(new_scale_text)
        if platform == 'android':
            android_util.reboot_android()
        else:
            app_data_dict['reset'] = True
            stopTouchApp()

def determine_screen_size():
    """
    determine_screen_size
    purpose: use tkinter to find screen size to fix Kivy screen scale issues
    returns: tuple of screen width and height, (0, 0) if not fullscreened
    """
    if platform in ('android', 'ios'):
        width = Window.width
        height = Window.height
    elif os.path.exists('no_fullscreen'):
        if os.path.exists('scale.kv'):
            with open('scale.kv', 'r') as file:
                line = file.readlines()
                width = int(line[0].split()[2])
                height = int(line[1].split()[2])
        else:
            width = 360
            height = 720
    else:
        from tkinter import Tk
        root = Tk()
        width = root.winfo_screenwidth()
        height = root.winfo_screenheight()
        root.destroy()
    with open('scale.kv', 'w') as file:
        file.write(f'#:set window_width {width}\n#:set window_height {height}\n')
    return width, height

def open_nav_drawer(self, *kwargs): # called from main.kv
    """
    open_nav_drawer
    args: self - self object
        kwargs - mystery arguments from KivyMD
    purpose: process navigation drawer open
    """
    app = App.get_running_app()
    if over_press.protect(app=app, vibrate=True):
        app.root.ids['nav_drawer'].set_state('open')

def select_screen(select_item): # called form kv file
    """
    select_screen
    args: select_item - navigator item widget selected
    purpose: provide a mechanism for navigating to a new screen
    """
    Logger.info('pantheon_util: select screen')
    app = App.get_running_app()
    try:
        unpickleable = app.app_data_dict['unpickleable']
        if select_item.selected:
            selected = app.navigation_map[select_item.text]
            if selected['screen']:
                    unpickleable['vibrator'].vibrate('button')
                    app.root.ids['screen_container'].clear_widgets()
                    app.root.ids['screen_container'].add_widget(selected['screen'])
                    app.title = selected['title']
                    app.root.ids['nav_drawer'].set_state(new_state='close')
        for screen in unpickleable.values():
            if isinstance(screen, TextInputUtil):
                screen.defocus_all()
    except Exception as e:
        Logger.info('pantheon_util: select_screen ignoring chicken/egg event exception: {}'.format(str(e)))
