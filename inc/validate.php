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
require_once 'inc/globals.php';


/**
 * Check that the session id provided by the user is valid and matches
 * the session id of the current PHP session.
 * @package validate
 * 
 * @param string $session_id the session_id of the post data.
 * @return boolean TRUE if the input for the session id is valid
 */
function valid_session_id($session_id)
{
    global $error_msg;

    if ($session_id === session_id())
    {
        return TRUE;
    }

    array_push($error_msg, 'Invalid Session ID: ' . $session_id);
    return FALSE;
}


/**
 * Check that the resolution provided by the user is valid and matches
 * one of the supported resolutions.
 * @package validate
 * 
 * @param string $resolution the resolution of the post data.
 * @return boolean TRUE if the input for the resolution is valid
 */
function valid_resolution($resolution)
{
    global $error_msg, $supported_resolutions;

    if (preg_match('/^[0-9]+x[0-9]+$/', $resolution)
        && in_array($resolution, $supported_resolutions))
    {
        return TRUE;
    }

    array_push($error_msg, 'Invalid Resolution: ' . $resolution);
    return FALSE;
}


/**
 * Check that the quantity of wallpapers requested by the user is valid and matches
 * one of the supported number of quantities of wallpapers that can be downloaded.
 * @package validate
 * 
 * @param string $quantity the quantity of wallpapers requested of the post data.
 * @return boolean TRUE if the input for the quantity is valid
 */
function valid_quantity($quantity)
{
    global $error_msg, $supported_quantities;

    if (preg_match('/^\d+$/', $quantity)
        && in_array($quantity, $supported_quantities))
    {
        return TRUE;
    }

    array_push($error_msg, 'Invalid Quantity: ' . $quantity);
    return FALSE;
}
?>