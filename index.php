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
require_once 'inc/validate.php';
require_once 'inc/globals.php';

session_start();


/* Connect to Redis and get the high and low resolution images */
$redis = new Redis();
if (! $redis->connect('127.0.0.1'))
{
    printf("Connection failed!\n");
    exit();
}


/* If the user submitted valid data submit the request as a new job */
if (isset($_POST['resolution']) && isset($_POST['quantity']) && isset($_POST['session_id']))
{
    /* If the data is valid then submit request to the queue */
    if (valid_resolution($_POST['resolution'])
        && valid_quantity($_POST['quantity'])
        && valid_session_id($_POST['session_id']))
    {
        $redis->set('job:' . $_POST['session_id'] . ':resolution', $_POST['resolution']);
        $redis->setTimeout('job:' . $_POST['session_id'] . ':resolution', $job_TTL);
        $redis->set('job:' . $_POST['session_id'] . ':quantity', $_POST['quantity']);
        $redis->setTimeout('job:' . $_POST['session_id'] . ':quantity', $job_TTL);
        $redis->zAdd('job:queue:uuids', round(microtime(true) * 1000), $_POST['session_id']);
        $redis->set('job:' . $_POST['session_id'] . ':progress', 0);
        $redis->setTimeout('job:' . $_POST['session_id'] . ':progress', $job_TTL);
    }
    /* Set the progress to -1 and store the error message in Redis */
    else
    {
        $redis->set('job:' . session_id() . ':error', $error_msg);
        $redis->setTimeout('job:' . session_id() . ':error', $job_TTL);
        $redis->set('job:' . session_id() . ':progress', -1);
        $redis->setTimeout('job:' . session_id() . ':progress', 2);
    }
}
/* User is loading the page, get a random background */
else
{
    $lowres_img = $redis->get('OgmgwkrrRK2lXUpVrmsh8Q:800x480');
    $highres_img = $redis->get('OgmgwkrrRK2lXUpVrmsh8Q:1920x1080');

     /* Display the header */
    include 'templates/header.php';

    /* The main body of the page */
    include 'templates/body.php';

    /* Include the footer */
    include 'templates/footer.php';
}

$redis->close();
?>