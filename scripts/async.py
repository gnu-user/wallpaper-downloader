#!/usr/bin/env python2
import pico
import uuid
import base64
import random
import json
from util import *

# Dictionary mapping images to resolutions and their location
images = {'OgmgwkrrRK2lXUpVrmsh8Q': {'800x480': 'img/02785_aspenwetland_800x480.jpg'}}

# queue of valid UUIDs to current jobs executed during the session
queue = {}


def hello():
    for i in xrange(3):
        yield i


def get_wallpaper():
    """Gets an initial random low-resolution image for the background
    """
    rand_uuid = random.choice(images.keys())
    return {'uuid': rand_uuid, 'name': images[rand_uuid]['800x480']}


def get_uuid():
    """Returns a unique identifier to the client which is used to
    fetch the compressed wallpapers when they're ready
    """
    new_uuid = generate_uuid()
    queue[new_uuid] = {'background': None, 'wallpapers': None}
    return new_uuid
