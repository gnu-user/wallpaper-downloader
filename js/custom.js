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
/* The root URL of the domain */
var rootURL = 'http://wallpaper.dom';

$(document).ready(function () {
    /* POST resolution and number of wallpapers and show progress bar */
    $('#btn_download').click(function(event) {
        /* Get the unique session id and POST data */
        var session_id = $('#session_id').val();
        var post_data = $('#download_form').serialize();

        /* Submit the data using AJAX POST and show progress bar */
        $.ajax({
            type: 'post',
            url: rootURL + '/index.php',
            data: post_data,
            success: function() {
                console.log(post_data);
                console.log(session_id);
                getProgress(session_id);
            }
        });
        event.preventDefault();
    });
});

/* A function which gets the progress of job preparing the wallpapers */
function getProgress(session_id)
{
    $('#progress_bar').css('width', '50%');
}

function logIt(data)
{
  console.log(data);
}