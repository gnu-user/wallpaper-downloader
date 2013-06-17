#!/usr/bin/env pypy
###############################################################################
#
# Manager for the backend of the wallpaper downloader, it processes
# requests submitted by users in the queue and dispatches the jobs to the
# appropriate process.
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
from multiprocessing import Pool, cpu_count, ProcessError, get_logger, log_to_stderr
from worker import *
import logging
import redis
import time
import sys


# Image and compressed zip file directories
image_dir = ''
output_dir = ''

# Default maximum number of jobs to execute in the pool
max_processes = cpu_count() * 2

# Process command line arguments
if len(sys.argv) < 3 or sys.argv[1] == '--help':
    sys.stderr.write("Usage: manager.py {image dir} {output dir} {max processes (optional)}\n")
    sys.stderr.write("Example: manager.py images/ files/ 16\n")
    sys.exit(2)
else:
    image_dir, output_dir = sys.argv[1:3]

    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if len(sys.argv) == 4:
        try:
            max_processes = int(sys.argv[1])
        except ValueError:
            sys.stderr.write("Invalid number of max processes!\n")
            sys.exit(1)


# Configure the logging, at the moment multiprocessing can ONLY log to console
log_to_stderr()
logger = get_logger()
logger.setLevel(logging.INFO)


# Create a pool of processes
pool = Pool(processes=max_processes, maxtasksperchild=4)

# Connect to the local Redis database
r = redis.StrictRedis(host='localhost')

# Every 500ms add any new jobs to the Pool of tasks to be executed
while True:
    for task in r.zrange('job:queue:uuids', 0, -1):
        # Add the uuid of the task to the pool and remove it from queue
        logger.info('Executing job: ' + task)
        pool.apply_async(prepare_download, [task, image_dir, output_dir])
        r.zrem('job:queue:uuids', task)

    time.sleep(1)
