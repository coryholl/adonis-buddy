#!/usr/bin/env python3
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
import os
from kivy.config import Config
#local import
import pantheon_util
import view

def main():
    """
    main
    purpose: provide main program function for app
    """
    Config.set('graphics', 'allow_screensaver', False)
    Config.set('kivy', 'exit_on_escape', False)
    if not os.path.exists('scale.kv'):
        with open('scale.kv', 'w') as file:
            file.write('#:set window_width 360\n#:set window_height 720\n')
    loop = True
    while loop:
        loop = run()

def run():
    data_root = {}
    data_root['window width'], data_root['window height'] = pantheon_util.determine_screen_size()
    app = view.AdonisBuddyApp(data_root)
    app.run()
    return True if 'reset' in data_root and data_root['reset'] else False

if __name__ == '__main__':
    main()

