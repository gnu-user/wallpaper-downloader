Wallpaper Downloader
====================

Automatically download wallpapers from various wallpaper websites.


Description
--------------

The wallpaper downloader is simple Python script I made a number of years ago when I was working on
family member's computers and realized that the following is a universal law of repairing family 
and friend's computers.

  ```
  Q = Nice Wallpapers
  P = Better Computer
  
  Q --> P 
  Q
  --------------------
  Therefore, P
  ```
  
How to Use Wallpaper Downloader
-------------------------------

To use the wallpaper downloader simply execute the script, provide the resolution of the wallpapers
you want as the first argument, the number of wallpapers to download as the second, and the directory
to store the wallpapers in as the third argument. By the way, if you re-run the script, **it does not
download the same wallpapers**, so running it consecutively will download more wallpapers each time.

  ```bash
  ./wallpaper-downloader 1680x1050 10 /home/user/pictures/
  ```
  
Currently only ***intefacelift.com*** is supported, I decided to support them first since they have
in my opinion the nicest wallpapers and I didn't need any other websites for my purpose. But if you
find some other sites you wish to be added then please let me know.

Supported Resolutions
-----------------------

Currently the following resolutions are supported, however it may be a long time or impossible to download
all of the wallpapers if you specify an uncommon resolution.

    2560x1600
    2560x1440
    1920x1200
    1680x1050
    1440x900
    1280x800
    1600x1200
    1400x1050
    1280x1024
    1280x960
    1024x768
    1920x1080
    1280x720
    1024x1024
    640x960
    320x480
    320x240
    1366x768
    1280x800
    1024x600
    800x480
    2560x1024
    2880x900
    3200x1200
    3360x1050
    3840x1200
    5120x1600
    3840x960
    3840x1024
    4320x900
    4096x1024
    4800x1200
    5040x1050
     
