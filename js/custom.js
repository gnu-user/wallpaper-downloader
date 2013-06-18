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

    /* Close the submit error on click */
    $('.alert .close').click( function() {
        $(this).parent().hide();
    });
});

/* Gets the progress of job preparing the wallpapers */
function getProgress(session_id, progress)
{
    progress = typeof progress !== 'undefined' ? progress : 0;

    setTimeout(function () {
        /* Display the current progress */
        $('#progress_bar').css('width', progress + '%');

        if (progress == -1) {
            /* Something went wrong or job cancelled, display any errors */
            $('#downloadModal').modal('hide');
            showError(session_id);
        }
        else if (progress < 100) {
            /* Get the job progress */
            $.ajax({
                type: 'GET',
                url: rootURL + '/api/progress/' + session_id,
                dataType: 'json',
                cache: false,
                success: function(data) {
                    getProgress(session_id, data);
                }
            });
        }
        else if (progress >= 100) {
            /* The file is ready get the file to download */
            $('#downloadModal').modal('hide');
            getDownload(session_id);
        }

    }, 1000);
}

/* Gets the wallpaper zip file download */
function getDownload(session_id)
{
    $.ajax({
        type: 'GET',
        url: rootURL + '/api/download/' + session_id,
        dataType: 'json',
        success: function(data) {
            window.location.assign(data);
        }
    });
}

/* Displays the error message */
function showError(session_id)
{
    $.ajax({
        type: 'GET',
        url: rootURL + '/api/error/' + session_id,
        dataType: 'json',
        success: function(data) {
            if (data.length > 1)
            {
                //if ($.trim($('#form-error').text()).length <= 1) {
                $('#form-error p').empty();
                $('#form-error').append('<p><strong>Error!</strong> ' + data + '</p>');

                /* Show the error for 5 seconds */
                $('#form-error').show();
                setTimeout(function() {
                    $("#form-error").hide()
                }, 5000);
            }
        }
    });
}