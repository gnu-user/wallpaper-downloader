#!/usr/bin/env pypy
###############################################################################
#
# Contains the classes which provide support for downloading wallpapers from
# various sources.
#
# Copyright (C) 2013, Jonathan Gillett
# All rights reserved.
#
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
import os
import subprocess
import urllib2
import re


class WallDownloader(object):
    """The base class for downloading wallpapers, it is inherited and overridden
    by classes which are tailored to downloading wallpapers from more specific
    sources. It provides support for downloading wallpapers specifically
    from Interfacelift.
    """
    """A list of supported resolutions and corresponding download pages"""
    _resolutions = {
        '2560x1600' : 'http://interfacelift.com/wallpaper/downloads/date/widescreen/2560x1600/',
        '2560x1440': 'http://interfacelift.com/wallpaper/downloads/date/widescreen/2560x1440/',
        '1920x1200': 'http://interfacelift.com/wallpaper/downloads/date/widescreen/1920x1200/',
        '1680x1050': 'http://interfacelift.com/wallpaper/downloads/date/widescreen/1680x1050/',
        '1440x900' : 'http://interfacelift.com/wallpaper/downloads/date/widescreen/1440x900/',
        '1280x800' : 'http://interfacelift.com/wallpaper/downloads/date/widescreen/1280x800/',
        '1600x1200': 'http://interfacelift.com/wallpaper/downloads/date/fullscreen/1600x1200/',
        '1400x1050': 'http://interfacelift.com/wallpaper/downloads/date/fullscreen/1400x1050/',
        '1280x1024': 'http://interfacelift.com/wallpaper/downloads/date/fullscreen/1280x1024/',
        '1280x960' : 'http://interfacelift.com/wallpaper/downloads/date/fullscreen/1280x960/',
        '1024x768' : 'http://interfacelift.com/wallpaper/downloads/date/fullscreen/1024x768/',
        '1920x1080': 'http://interfacelift.com/wallpaper/downloads/date/hdtv/1080p/',
        '1280x720' : 'http://interfacelift.com/wallpaper/downloads/date/hdtv/720p/',
        '1024x1024': 'http://interfacelift.com/wallpaper/downloads/date/apple_devices/ipad_1024x1024/',
        '640x960'  : 'http://interfacelift.com/wallpaper/downloads/date/apple_devices/iphone_4_640x960/',
        '320x480'  : 'http://interfacelift.com/wallpaper/downloads/date/apple_devices/iphone,_3g,_3gs/',
        '320x240'  : 'http://interfacelift.com/wallpaper/downloads/date/apple_devices/ipod_touch/',
        '1366x768' : 'http://interfacelift.com/wallpaper/downloads/date/netbook/1366x768/',
        '1280x800' : 'http://interfacelift.com/wallpaper/downloads/date/netbook/1280x800/',
        '1024x600' : 'http://interfacelift.com/wallpaper/downloads/date/netbook/1024x600/',
        '800x480'  : 'http://interfacelift.com/wallpaper/downloads/date/netbook/800x480/',
        '2560x1024': 'http://interfacelift.com/wallpaper/downloads/date/2_screens/2560x1024/',
        '2880x900' : 'http://interfacelift.com/wallpaper/downloads/date/2_screens/2880x900/',
        '3200x1200': 'http://interfacelift.com/wallpaper/downloads/date/2_screens/3200x1200/',
        '3360x1050': 'http://interfacelift.com/wallpaper/downloads/date/2_screens/3360x1050/',
        '3840x1200': 'http://interfacelift.com/wallpaper/downloads/date/2_screens/3840x1200/',
        '5120x1600': 'http://interfacelift.com/wallpaper/downloads/date/2_screens/5120x1600/',
        '3840x960' : 'http://interfacelift.com/wallpaper/downloads/date/3_screens/3840x960/',
        '3840x1024': 'http://interfacelift.com/wallpaper/downloads/date/3_screens/3840x1024/',
        '4320x900' : 'http://interfacelift.com/wallpaper/downloads/date/3_screens/4320x900/',
        '4096x1024': 'http://interfacelift.com/wallpaper/downloads/date/3_screens/4096x1024/',
        '4800x1200': 'http://interfacelift.com/wallpaper/downloads/date/3_screens/4800x1200/',
        '5040x1050': 'http://interfacelift.com/wallpaper/downloads/date/3_screens/5040x1050/'
    }

    def __init__(self, directory=''):
        """Initialize the default wallpaper downloader, which only support downloading from interfacelift

        :param directory: The name of the directory to store the results in, otherwise directory name is resolution
        :type directory: str
        """
        self.site_url = 'http://interfacelift.com'
        self.useragent = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 (.NET CLR 3.5.30729)'
        self.directory = directory
        self.opener = urllib2.build_opener()
        self.opener.addheaders = [('User-agent', self.useragent)]

    @classmethod
    def resolutions(self):
        """Returns the list of supported resolutions"""
        return self._resolutions

    @classmethod
    def get_filename(self, file):
        """Gets the raw, unique part of the filename (without the resolution component)
        in order to easily identify the same image but at different resolutions.
        """
    return re.search(r'/([^/]+)_\d+x\d+.*\.jpg', file).group(1)

    def downloads(self, resolution, quantity):
        """An iterator which returns the path and filename of each wallpaper downloaded,
        in the event that there are not enough wallpapers available to meet the quantity
        requested a StopIterator exception is thrown.

        :param resolution: The resolution of the wallpapers to download, if it is not one of the supported
        resolutions a KeyError exception is thrown. Each wallpaper downloaded is stored in a directory with
        the same name as the resolution, to change this provide constructor with the directory to use!
        :type resolution: str

        :param quantity: The quantity of wallpapers to download.
        :type quantity: str
        """
        if not resolution in self._resolutions:
            raise KeyError('The resolution: ' + resolution + ' is unsupported!')

        self.directory = os.path.join(os.path.normpath(self.directory), resolution)
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

        downloads = 0
        # Download the quantity of wallpapers specified, yield the path and name
        for filename, download_url in self.get_wallpaper(resolution):
            if downloads >= quantity:
                break

            if filename == '' or download_url == '':
                raise StopIteration('Could not download all wallpapers, no more available!')

            # Check that the file hasn't already been downloaded
            if os.path.exists(os.path.join(os.path.normpath(self.directory), filename)):
                #print 'File already exists, skipping to the next file to download.'
                continue
            else:
                # Download the picture to local directory
                os.system('wget -P ' + self.directory + ' -nc -U "' + self.useragent + '" ' + download_url + ' &> /dev/null')
                downloads += 1
                #print "# OF DOWNLOADS: " + str(downloads)
                yield os.path.join(os.path.normpath(self.directory), filename)

    def get_wallpaper(self, resolution):
        """An internal method which is used to fetch wallpaper download URLs from
        interfacelift for the resolution specified. An empty URL is returned in the
        event that there are no more wallpapers available for the resolution.

        :param resolution: The resolution of the wallpapers to download.
        :type resolution: str
        """
        # Get the URL of the specific resolution wallpapers
        url = self._resolutions[resolution]
        page_count = 1
        while True:
            #print "CURRENT PAGE URL: " + url + "index" + str(page_count) + ".html"
            data = self.opener.open(url + "index" + str(page_count) + ".html").read()
            currentpos = 0

            # If there are no more pages to download from return empty URL
            if not data:
                return

            # Get the randomly generated string that appears in the url after wallpaper/
            if re.findall(r".+((<a\shref\=\"/wallpaper/\w+/)\w+\.jpg)", data):
                m = re.findall(r".+((<a\shref\=\"/wallpaper/\w+/)\w+\.jpg)", data)
                start = m[0][1]
                #print start

            # Each page of interfacelift contains a maximum of 10 images
            for n in xrange(0, 10):
                    index = data.find(start, currentpos)
                    if index == -1:
                        break
                    endofindex = data.find('">', index)
                    currentpos = index + 1

                    # Get the filename from href using regex
                    #print data[index:endofindex]
                    #print data[index+9:endofindex]
                    if re.match(r"^.+/(\w+\.jpg)", data[index:endofindex]):
                        n = re.match(r"^.+/(\w+\.jpg)", data[index:endofindex])
                        filename = n.group(1)
                        download_url = self.site_url + data[index+9:endofindex]
                        #print "File: " + filename
                        #print "URL: " + download_url
                        # Yield the filename and the download url
                        yield (filename, download_url)

            page_count += 1
