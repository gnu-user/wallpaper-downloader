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
session_start();


/* Connect to Redis and get the high and low resolution images */
$redis = new Redis();
$redis->connect('127.0.0.1'); // port 6379 by default

$lowres_img = $redis->get('OgmgwkrrRK2lXUpVrmsh8Q:800x480');
$highres_img = $redis->get('OgmgwkrrRK2lXUpVrmsh8Q:1920x1080');
$session_id = session_id();

print_r($_POST);

 /* Display the header */
include 'templates/header.php';

/* The main body of the page */
include 'templates/body.php';

/* Include the footer */
include 'templates/footer.php';

?>