<?php
/*
 * Copyright (C) 2013, Jonathan Gillett
 * All rights reserved.
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program. If not, see <http://www.gnu.org/licenses/>.
 */

/* Contains a list of global variables, these are mainly used to simplify validation
 * of data submitted, such as the supported resolutions, and maximum number of
 * downloads allowed without having to pass around the same arguments to multiple
 * functions
 */
$error_msg;

$supported_resolutions = array('1280x800', '800x600', '720x1280', '480x800', 
                              '320x480', '1600x1200', '1400x1050', '1280x960', 
                              '1024x768', '1280x1024', '1366x768', '1024x600', 
                              '2880x1800', '2560x1600', '1920x1200', '1680x1050', 
                              '1440x900', '1280x800', '2560x1440', '1920x1080', 
                              '1600x900', '1280x720');

$supported_quantities = array(5, 10, 25, 50);

/* The TTL for jobs added to Redis, currently 4 hours */
$job_TTL = 14400;

?>