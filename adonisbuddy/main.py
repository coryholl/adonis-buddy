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
import sys
if sys.version_info >= (3, 10):
    sys.path.insert(0, os.path.join('..', 'pantheon_lib'))
    sys.path.insert(0, '.')
    import adonis_buddy

    if __name__ == '__main__':
        adonis_buddy.main()
else:
    print('Adonis Buddy requires Python 3.10 or higher.')
    sys.exit(1)
