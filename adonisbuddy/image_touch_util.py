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

import os
from kivy.app import App
from kivy.logger import Logger
#local imports
import over_press

class ImageTouchUtil:

    def select_image(self, name):
        """
        select_image
        args: self - self object
            name - name of muscle
        purpose: set form for selected image
        """
        app = App.get_running_app()
        self.ids['select_image_id'].source = os.path.join('images',
            app.app_data_dict['unpickleable']['image map'][name][self.screen_name]['display image file'])

    def touched(self, image, touch):
        """
        touched
        args: self - self object
            image - image object touched
            touch - touch object
        purpose: process the touch of the body measurement image
        """
        Logger.info(f'image_touch_util: touched: image: {image} touch: {touch}')
        if (image.collide_point(touch.x, touch.y) and not (self.ids['keypad_button_container_id'].children and
                    self.ids['keypad_button_container_id'].children[0].collide_point(touch.x, touch.y))):
            app = App.get_running_app()
            if over_press.protect(app=app, vibrate=True):
                binding_box_ratio = image.width / image.height
                if binding_box_ratio >= image.image_ratio:
                    scale = image.size[1] / image.texture_size[1]
                    x_padding = (image.size[0] - (image.texture_size[0] * scale)) / 2
                    x_coord = (touch.x - x_padding) / scale
                    y_coord = image.texture_size[1] - (touch.y / scale)
                    if 0 <= x_coord < image.texture_size[0] and 0 <= y_coord < image.texture_size[1]:
                        for name, muscle in app.app_data_dict['unpickleable']['image map'].items():
                            if self.screen_name in muscle:
                                color = muscle[self.screen_name]['core image'].read_pixel(x_coord, y_coord)
                                muscle[self.screen_name]['selected'] = True if color[3] else False
                                if muscle[self.screen_name]['selected']:
                                    self.select_image(name)
