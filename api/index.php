<?php 
/*
 * CS-CLUB Elections Website
*
* Copyright (C) 2013 Jonathan Gillett, Joseph Heron, Computer Science Club at DC and UOIT
* All rights reserved.
*
* This program is free software: you can redistribute it and/or modify
* it under the terms of the GNU Affero General Public License as
* published by the Free Software Foundation, either version 3 of the
* License, or (at your option) any later version.
*
* This program is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* GNU Affero General Public License for more details.
*
* You should have received a copy of the GNU Affero General Public License
* along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/
require 'Slim/Slim.php';
\Slim\Slim::registerAutoloader();


/*
 * The REST web service api which provides access to get the progress of jobs
 * and the final compressed zip file of images when they are ready for download
 */
$app = new \Slim\Slim();

/* Gets the progress of a download request submitted by a user */
$app->get('/progress/:session_id', 'getProgress');
$app->get('/error/:session_id', 'getError');
$app->get('/download/:session_id', 'getDownload');

$app->run();


/** 
 * Get the progress of a download request submitted by the user
 * @package api
 *
 * @param string $session_id The session id of the user who submitted the request
 */
function getProgress($session_id)
{
	global $db_user, $db_pass, $db_elec_name;

	/* Connect to Redis */
	$redis = new Redis();

	/* check connection */
	if (! $redis->connect('127.0.0.1'))
	{
	    printf("Connection failed!\n");
	    exit();
	}

	/* Get the progress of the job */
	echo json_encode($redis->get('job:' . $session_id . ':progress'));
}


/** 
 * Get the list of errors messages in the event that there was an error.
 * @package api
 *
 * @param string $session_id The session id of the user who submitted the request
 */
function getError($session_id)
{
	global $db_user, $db_pass, $db_elec_name;

	/* Connect to Redis */
	$redis = new Redis();

	/* check connection */
	if (! $redis->connect('127.0.0.1'))
	{
	    printf("Connection failed!\n");
	    exit();
	}

	/* Get the progress of the job */
	echo json_encode($redis->get('job:' . $session_id . ':error'));
}


/** 
 * Get the location of the file to download for the request submitted by the user
 * @package api
 *
 * @param string $session_id The session id of the user who submitted the request
 */
function getDownload($session_id)
{
	global $db_user, $db_pass, $db_elec_name;

	/* Connect to Redis */
	$redis = new Redis();

	/* check connection */
	if (! $redis->connect('127.0.0.1'))
	{
	    printf("Connection failed!\n");
	    exit();
	}

	/* Get the progress of the job */
	echo json_encode($redis->get('job:' . $session_id . ':file'));
}
?>