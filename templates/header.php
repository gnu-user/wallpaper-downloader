<?php
/*
 * The header for the wallpaper bulk downloader
 * 
 * 
 * DEPENDENCIES
 * ------------
 * 
 * Depends on the $highres_img and $lowres_img being set in order to have the background
 * for the website load a random wallpaper each time. The same wallpaper is loaded with
 * a low resolution version and a higher resolution of the same image replaces it when
 * the page has fully loaded
 *
 */
?>
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <meta charset="utf-8">
    <title>
      Bulk Wallpaper Downloader
    </title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Download a zip of randomly selected HD wallpapers">
    <meta name="author" content="Two Guys With Spare Time"><!-- Le styles -->
    <link href="css/bootstrap.min.css" rel="stylesheet">
    <link href="css/bootstrap-responsive.min.css" rel="stylesheet">
    <link href="css/custom.css" rel="stylesheet">
    <link rel="shortcut icon" href="favicon.ico">
    <!-- HTML5 shiv, for IE6-8 support of HTML5 elements -->
    <!--[if lt IE 9]>
      <script src="js/html5shiv.min.js"></script>
      <style style="text/css">
        #wallpaper {
              filter: progid:DXImageTransform.Microsoft.AlphaImageLoader(src='.myBackground.jpg', sizingMethod='scale');
              -ms-filter: "progid:DXImageTransform.Microsoft.AlphaImageLoader(src='myBackground.jpg', sizingMethod='scale')";
        }
    </style>
    <![endif]-->
  </head>