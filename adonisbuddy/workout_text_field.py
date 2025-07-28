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
from kivymd.uix.textfield import MDTextField

__version__ = '1,0.0'

class WorkoutTextField(MDTextField):

    def on_selection_text(self, *kwargs):
        """
        on_selection_text
        args: self - self object
            kwargs - unknonw args
        purpose: disable text selection feature
        """
        self.cancel_selection()
