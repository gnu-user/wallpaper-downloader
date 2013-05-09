#!/usr/bin/env python2

###############################################################################
#
#  A simple Python script which downloads wallpapers from websites that have 
#  nice wallpapers. Currently the only website supported is interfacelift.com
#
#  TODO: Implement the equivalent for DeviantArt and OTHERWEBSITES
#
#
#  Copyright (C) 2013, Jonathan Gillett
#  All rights reserved.
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
import os
import urllib2
import re
import sys

url         = ''
directory   = ''
start       = ''  # Start of the html <a href=""> tag for the image, a regex is used to get this
end         = '">'
useragent   = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 (.NET CLR 3.5.30729)'
filename    = ''
limit       = 0
downloads   = 0
page_count  = 1
resolutions = {'2560x1600' : "http://interfacelift.com/wallpaper/downloads/date/widescreen/2560x1600/",
               '2560x1440' : "http://interfacelift.com/wallpaper/downloads/date/widescreen/2560x1440/",
               '1920x1200' : "http://interfacelift.com/wallpaper/downloads/date/widescreen/1920x1200/",
               '1680x1050' : "http://interfacelift.com/wallpaper/downloads/date/widescreen/1680x1050/",
               '1440x900'  : "http://interfacelift.com/wallpaper/downloads/date/widescreen/1440x900/",
               '1280x800'  : "http://interfacelift.com/wallpaper/downloads/date/widescreen/1280x800/",
               '1600x1200' : "http://interfacelift.com/wallpaper/downloads/date/fullscreen/1600x1200/",
               '1400x1050' : "http://interfacelift.com/wallpaper/downloads/date/fullscreen/1400x1050/",
               '1280x1024' : "http://interfacelift.com/wallpaper/downloads/date/fullscreen/1280x1024/",
               '1280x960'  : "http://interfacelift.com/wallpaper/downloads/date/fullscreen/1280x960/",
               '1024x768'  : "http://interfacelift.com/wallpaper/downloads/date/fullscreen/1024x768/",
               '1920x1080' : "http://interfacelift.com/wallpaper/downloads/date/hdtv/1080p/",
               '1280x720'  : "http://interfacelift.com/wallpaper/downloads/date/hdtv/720p/",
               '1024x1024' : "http://interfacelift.com/wallpaper/downloads/date/apple_devices/ipad_1024x1024/",
               '640x960'   : "http://interfacelift.com/wallpaper/downloads/date/apple_devices/iphone_4_640x960/",
               '320x480'   : "http://interfacelift.com/wallpaper/downloads/date/apple_devices/iphone,_3g,_3gs/",
               '320x240'   : "http://interfacelift.com/wallpaper/downloads/date/apple_devices/ipod_touch/",
               '1366x768'  : "http://interfacelift.com/wallpaper/downloads/date/netbook/1366x768/",
               '1280x800'  : "http://interfacelift.com/wallpaper/downloads/date/netbook/1280x800/",
               '1024x600'  : "http://interfacelift.com/wallpaper/downloads/date/netbook/1024x600/",
               '800x480'   : "http://interfacelift.com/wallpaper/downloads/date/netbook/800x480/",
               '2560x1024' : "http://interfacelift.com/wallpaper/downloads/date/2_screens/2560x1024/",
               '2880x900'  : "http://interfacelift.com/wallpaper/downloads/date/2_screens/2880x900/",
               '3200x1200' : "http://interfacelift.com/wallpaper/downloads/date/2_screens/3200x1200/",
               '3360x1050' : "http://interfacelift.com/wallpaper/downloads/date/2_screens/3360x1050/",
               '3840x1200' : "http://interfacelift.com/wallpaper/downloads/date/2_screens/3840x1200/",
               '5120x1600' : "http://interfacelift.com/wallpaper/downloads/date/2_screens/5120x1600/",
               '3840x960'  : "http://interfacelift.com/wallpaper/downloads/date/3_screens/3840x960/",
               '3840x1024' : "http://interfacelift.com/wallpaper/downloads/date/3_screens/3840x1024/",
               '4320x900'  : "http://interfacelift.com/wallpaper/downloads/date/3_screens/4320x900/",
               '4096x1024' : "http://interfacelift.com/wallpaper/downloads/date/3_screens/4096x1024/",
               '4800x1200' : "http://interfacelift.com/wallpaper/downloads/date/3_screens/4800x1200/",
               '5040x1050' : "http://interfacelift.com/wallpaper/downloads/date/3_screens/5040x1050/"}

if len(sys.argv) < 4:
    # print help information and exit
    print "not enough arguments given!"
    print "Usage: wallpaper-downloader [Resolution] [# Of Images to Download] [Directory to Download the files to]"
    print "Example: wallpaper-downloader 1680x1050 10 /home/user/pictures/"
    sys.exit()

# Validate that each argument is correct
if sys.argv[1] in resolutions:
    # Set the default url to the specified resolution
    url = resolutions[sys.argv[1]]
else:
    # Resolution false, or not supported
    print "The resolution: " + sys.argv[1] + " is either invalid or not supported!"
    print "Please try using one of the following supported resolutions:"
    print sorted(resolutions.keys())
    sys.exit()

if sys.argv[2].isdigit():
    # Set the limit for the number of images to download
    limit = int(sys.argv[2])
else:
    # Invalid entry
    print "Please enter a valid amount of pictures to download, such as 25"
    sys.exit()
    
if os.path.exists(sys.argv[3]):
    # Set the download directory
    directory = sys.argv[3]
else:
    # Directory does not exist
    print "The directory: " + sys.argv[3] + " does not exist!" 
    sys.exit()

# Create opener and specify user agent, fix for server returning 403
opener = urllib2.build_opener()
opener.addheaders = [('User-agent', useragent)]

while True:
        print "CURRENT PAGE URL: " + url + "index" + str(page_count) + ".html"
        data       = opener.open(url + "index" + str(page_count) + ".html").read()
        currentpos = 0
        
        # If there are no more pages to download from quit
        if not data:
            quit()

        # Get the randomly generated string that appears in the url after wallpaper/
        if re.findall(r".+((<a\shref\=\"/wallpaper/\w+/)\w+\.jpg)", data):
            m = re.findall(r".+((<a\shref\=\"/wallpaper/\w+/)\w+\.jpg)", data)
            start = m[0][1]
            print start
        
        # Each page of interfacelift contains a maximum of 10 images
        for n in range(0,10):
                # If number of images downloaded has reached the limit quit  
                if downloads == limit:
                    quit()
                
                print "# OF DOWNLOADS: " + str(downloads)
                    
                index = data.find(start, currentpos)
                if index == -1:
                        break
                endofindex = data.find(end, index)
                currentpos = index + 1
                
                # Get the filename from href using regex
                print data[index:endofindex]
                print data[index+9:endofindex]
                if re.match(r"^.+/(\w+\.jpg)", data[index:endofindex]):
                    n = re.match(r"^.+/(\w+\.jpg)", data[index:endofindex])
                    filename = n.group(1)
                    print filename
                
                # Check that the file hasn't already been downloaded    
                if os.path.exists(directory + filename):
                        print 'File already exists, skipping to the next file to download.'
                        continue
                else:    
                    # Download the picture to local directory
                    os.system('wget -P ' + directory + ' -nc -U "' + useragent + '" ' + 'http://interfacelift.com' + data[index+9:endofindex])
                    downloads += 1
        page_count += 1
