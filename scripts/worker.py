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
from multiprocessing import get_logger
from wand.image import Image
from walldownloader import *
from util import *
import logging
from zipfile import ZipFile
import redis
import sys
import os

# The maximum number of wallpapers for each resolution to download
max_wallpapers = 250

# The TTL for jobs added to Redis, currently 4 hours
job_TTL = 14400


def prepare_download(task, image_dir, output_dir):
    """Prepares a download request submitted by a user, fetches a random set
    of wallpapers based on the resolution and number of wallpapers specified and
    creates a compressed zip file for download.
    """
    # Connect to the local Redis database, get logger
    r = redis.StrictRedis(host='localhost')
    logger = get_logger()

    # Get the resolution and number of downloads requested
    resolution = r.get('job:' + task + ':resolution')
    quantity = int(r.get('job:' + task + ':quantity'))

    # Exit if the job timed out (resolution and quantity requested no longer exist)
    # This should not happen unless the system is under heavy load, log issue
    if not resolution or not quantity:
        logger.warning('Job: ' + task + ' No resolution or quantity, job expired?')
        sys.exit(1)

    # Download more wallpapers if there are not enough for the resolution
    if r.scard('image:' + resolution + ':uuids') < max_wallpapers:
        logger.info('Job: ' + task + ' Downloading: ' + resolution + ' wallpapers!')
        download_wallpapers(r, task, image_dir, resolution, quantity)

    # Get a random set of wallpapers and create a zip file
    wallpapers = []
    for uuid in r.srandmember('image:' + resolution + ':uuids', quantity):
        wallpapers.append(r.get('image:' + uuid + ':' + resolution))

    logger.info('Job: ' + task + ' Wallpapers: ' + ', '.join(wallpapers))

    # Create a zip file, set key in redis
    compress_wallpapers(r, task, output_dir, wallpapers)

    sys.exit(0)


def download_wallpapers(r, task, image_dir, resolution, quantity):
    """Downloads a number of wallpapers based on the resolution and quantity
    and adds each new wallpaper to the Redis database. For any wallpapers that
    are 1080p a low resolution version is created and the pair of images
    is added to the list of background images.
    """
    logger = get_logger()
    wall = WallDownloader(image_dir)
    for wallpaper in wall.downloads(resolution, quantity):
        logger.info("Wallpaper: " + wallpaper + " downloaded!")
        r.incrbyfloat('job:' + task + ':progress', 75.0 / quantity)

        image_name = get_filename(wallpaper)
        uuid = r.get('image:' + image_name + ':uuid')

        if not uuid:
            uuid = generate_uuid()
            r.set('image:' + image_name + ':uuid', uuid)

        # Add the image to the list for the current resolution
        r.set('image:' + uuid + ':' + resolution, wallpaper)
        r.sadd('image:' + resolution + ':uuids', uuid)

        # Add 1080p images to list of background images
        if resolution == '1920x1080':
            create_background(r, task, uuid, image_dir, image_name)


def compress_wallpapers(r, task, output_dir, wallpapers):
    """Compresses the wallpapers into a zip file and sets the path to download
    the zipfile in the database.
    """
    logger = get_logger()
    file = os.path.join(os.path.normpath(output_dir), generate_uuid() + '.zip')
    logger.info('Job: ' + task + ' Creating compressed file: ' + file)

    with ZipFile(file, 'w') as zip:
        for wallpaper in wallpapers:
            zip.write(wallpaper, arcname=os.path.basename(wallpaper))
            r.incrbyfloat('job:' + task + ':progress', 24.0 / len(wallpapers))

    logger.info('Job: ' + task + ' Compressed file: ' + file + ' Ready!')
    r.setex('job:' + task + ':file', job_TTL, file)
    r.incrbyfloat('job:' + task + ':progress', 2.0)


def create_background(r, task, uuid, image_dir, image_name):
    """Creates a low resolution version of a 1080p wallpaper provided and saves
    the matching pair of images to the list of background images that are
    randomly displayed on the website.
    """
    logger = get_logger()

    # Get the wallpaper file path
    uuid = r.get('image:' + image_name + ':uuid')
    file = r.get('image:' + uuid + ':1920x1080')

    new_img_dir = os.path.join(os.path.normpath(image_dir), '800x480')
    new_file = os.path.join(os.path.normpath(new_img_dir), image_name + '_800x480.jpg')

    if not os.path.exists(new_img_dir):
            os.makedirs(new_img_dir)

    # Resize the image as 800x480 at 50% quality, save as new image
    logger.info('Job: ' + task + ' UUID: ' + uuid + ', creating background: ' + new_file)
    with Image(filename=file) as img:
        with img.clone() as new_img:
            new_img.compression_quality = 50
            new_img.resize(800, 480)
            new_img.save(filename=new_file)

    # Add the new background to the list
    r.set('image:' + uuid + ':800x480', new_file)
    r.sadd('image:backgrounds:uuids', uuid)
