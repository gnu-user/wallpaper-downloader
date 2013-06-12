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
from multiprocessing import Pool, cpu_count, ProcessError
from worker import *
import logging
import redis
import time
import sys


# The maximum number of jobs to execute in the pool
max_processes = cpu_count() * 2

# Create a pool of processes
pool = Pool(processes=max_processes, maxtasksperchild=4)

# Connect to the local Redis database
r = redis.StrictRedis(host='localhost')

# Every 500ms add any new jobs to the Pool of tasks to be executed
while True:
    for task in r.zrange('job:queue:uuids', 0, -1):
        # Add the uuid of the task to the pool and remove it from queue
        pool.apply_async(prepare_download, [task])
        #r.zrem('job:queue:uuids', task)

    time.sleep(1)
