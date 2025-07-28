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
from collections import OrderedDict
from kivy.core.image import Image as CoreImage
# local imports
import database
import database_util

class DataDict:

    def get_data_dict(self, data_dict):
        """
        get_data_dict
        args: self - self object
            data_dictionary to populate
        purpose: create application data dictionary
        """
        db = database.Database()
        data_dict['config'] = database_util.get_config(db.app_db)
        birth_date = db.get_birth_date()
        birth_date = birth_date[0]['value'] if birth_date else 'NOT SET'
        data_dict['global properties'] = {
            'birth date': birth_date,
            'last button press time': 0
        }
        data_dict['unpickleable'] = {
                'database': db,
                'data dictionary': self,
                'image map': self.get_image_maps(db)
            }

    def get_image_maps(self, db):
        """
        get_image_maps
        args: self - self object
            db - database object
        purpose: retrieve the database
        """
        images_items = db.get_circumference_images()
        circumference_maps = OrderedDict()
        for image_map in images_items:
            if image_map['display']:
                if image_map['body_part_name'] not in circumference_maps:
                    circumference_maps[image_map['body_part_name']] = {}
                circumference_maps[image_map['body_part_name']][image_map['screen']] = {
                    'core image': CoreImage(os.path.join('images', image_map['touch_image']), keep_data=True),
                    'display image file': image_map['selected_image'],
                    'selected': False,
                    'touch image file': image_map['touch_image']
                }
        return circumference_maps
