#!/usr/bin/env pypy
###############################################################################
#
# Worker for the backend of the wallpaper downloader, it executes requests
# submitted by users, fetches a random set of wallpapers and creates a
# compressed zip file for download.
#
# Copyright (C) 2013, Jonathan Gillett
# All rights reserved.
#
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
import logging
import redis
import time
import sys

# The maximum number of wallpapers for each resolution to download
max_wallpapers = 250


def prepare_download(task):
    """Prepares a download request submitted by a user, fetches a random set
    of wallpapers based on the resolution and number of wallpapers specified and
    creates a compressed zip file for download.
    """
    # Connect to the local Redis database
    r = redis.StrictRedis(host='localhost')

    # Get the resolution and number of downloads requested
    resolution = r.get('job:' + task + ':resolution')
    quantity = r.get('job:' + task + ':quantity')

    # Process the job if the resolution and quantity exist
    if resolution and quantity:
        if r.scard('image:' + resolution + ':uuids') < max_wallpapers:
            download_wallpapers(r, resolution, quantity)

    # Get a random set of wallpapers and create a zip file
    wallpapers = []
    for uuid in r.srandmember('image:' + resolution + ':uuids'):
        wallpapers.append(r.get('image:' + uuid + ':resolution'))

    # Create a zip file, set key in redis
    # set progress to 100
    # if resolution == 1080p create low res versions and add to backgrounds list


def download_wallpapers(r, resolution, quantity):
    """Downloads a number of wallpapers based on the resolution and quantity
    and adds each new wallpaper to the Redis database.
    """
    print resolution, quantity
