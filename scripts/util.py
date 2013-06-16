#!/usr/bin/env python2
###############################################################################
#
#  A set of utility method and other helpful functions.
#
#  Copyright (C) 2013, Jonathan Gillett
#  All rights reserved.
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
import re
import uuid
import base64


def generate_uuid():
    """Generate a Base64 encoded UUID which can be used safely as a key
    """
    r_uuid = base64.urlsafe_b64encode(uuid.uuid4().bytes)
    return re.sub(r'[\=\+\-\_\/]', '', r_uuid)


def get_filename(file):
    """Gets the raw, unique part of the filename (without the resolution component)
    in order to easily identify the same image but at different resolutions.
    """
    return re.search(r'/([^/]+)_\d+x\d+.*\.jpg', file).group(1)
