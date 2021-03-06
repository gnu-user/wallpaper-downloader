<?php
/*
 * The main body of the page for the wallpaper bulk downloader
 * 
 * 
 * DEPENDENCIES
 * ------------
 * 
 * Depends on a session being started, so session_id() method can be used to get a unique
 * session id when a job is submitted to fetch wallpapers.
 * 
 * Depends on the $highres_img being set in order to have the link
 * to download the background.
 *
 */
?>
  <!-- LE CONTENT NOW STARTS HERE -->
  <body id="wallpaper" class="background">
    <div class="container-narrow">
      <div class="jumbotron">
        <h1>
          Bulk Wallpaper Downloader
        </h1>
        <p class="lead">
          Download a zip of randomly selected HD wallpapers
        </p>
      </div>
      <div class="row-fluid marketing">
        <div class="span12">
          <form id="download_form" class="well well-small" action="index.php" method="post" accept-charset="UTF-8">
            <center>
              <br />
              <h4>Please select a resolution and quantity.</h4>
              <select name="resolution" class="select">
                <option value="">Select Resolution</option>
                <optgroup label="Mobile Devices">
                  <option id="res_1280x800" value="1280x800">1280x800 Tablet</option>
                  <option id="res_800x600" value="800x600">800x600 Tablet</option>
                  <option id="res_720x1280" value="720x1280">720x1280 Phone</option>
                  <option id="res_480x800" value="480x800">480x800 Phone</option>
                  <option id="res_320x480" value="320x480">320x480 Phone</option>
                </optgroup>
                <optgroup label="Fullscreen 4:3">
                 <option id="res_1600x1200" value="1600x1200">1600x1200</option>
                 <option id="res_1400x1050" value="1400x1050">1400x1050</option>
                 <option id="res_1280x960" value="1280x960">1280x960</option>
                 <option id="res_1024x768" value="1024x768">1024x768</option>
               </optgroup>
               <optgroup label="Fullscreen 5:4">
                <option id="res_1280x1024" value="1280x1024">1280x1024</option>
                </optgroup>
                <optgroup label="Notebooks">
                 <option id="res_1366x768" value="1366x768">1366x768</option>
                 <option id="res_1024x600" value="1024x600">1024x600</option>
               </optgroup>
               <optgroup label="Widescreen 16:10">
                 <option id="res_2880x1800" value="2880x1800">2880x1800 (Retina MacBook Pro)</option>
                 <option id="res_2560x1600" value="2560x1600">2560x1600</option>
                 <option id="res_1920x1200" value="1920x1200">1920x1200</option>
                 <option id="res_1680x1050" value="1680x1050">1680x1050</option>
                 <option id="res_1440x900" value="1440x900">1440x900</option>
                 <option id="res_1280x800_1" value="1280x800">1280x800</option>
               </optgroup>
               <optgroup label="Widescreen 16:9">
                 <option id="res_2560x1440" value="2560x1440">2560x1440</option>
                 <option id="res_1920x1080" value="1920x1080">1920x1080 (1080p HDTV)</option>
                 <option id="res_1600x900" value="1600x900">1600x900</option>
                 <option id="res_1280x720" value="1280x720">1280x720 (720p HDTV)</option>
               </optgroup>
              </select>
              <select name="quantity" class="select">
                <option value="">Select Quantity</option>
                <option id="wall_5" value="5">5 Wallpapers</option>
                <option id="wall_10" value="10">10 Wallpapers</option>
                <option id="wall_25" value="25">25 Wallpapers</option>
                <option id="wall_50" value="50">50 Wallpapers</option>
              </select>
              <input type="hidden" id="session_id" name="session_id" value="<?php echo session_id() ?>"/>
              <div id="form-error" class="span8 center alert alert-error fade in" style="display:none;">
                <button class="close" type="button">&times;</button>
              </div>
              <div class="row-fluid marketing">
                <div class="span12">
                  <center>
                    <div class="container-button">
                      <a id="btn_about" class="btn btn-large btn-info" href="#myModal" data-toggle="modal">About</a>
                      <button id="btn_download" class="btn btn-large btn-success" href="#downloadModal" data-toggle="modal">Download</button>
                    </div>
                    <hr>
                    <p>
                      Like the current background? <a href="<?php echo $highres_img ?>" target="_blank">Right click here and "Save Link As"</a>
                    </p>
                  </center>
                </div>
                <div class="span12">
                  <center>
                    <span class='st_facebook_large' displayText='Facebook'></span>
                    <span class='st_twitter_large' displayText='Tweet'></span>
                    <span class='st_pinterest_large' displayText='Pinterest'></span>
                    <span class='st_stumbleupon_large' displayText='StumbleUpon'></span>
                    <span class='st_tumblr_large' displayText='Tumblr'></span>
                    <span class='st_wordpress_large' displayText='WordPress'></span>
                    <span class='st_googleplus_large' displayText='Google +'></span>
                    <br />
                    <p>&copy; 2013 Two Guys With Spare Time</p>
                  </center>
                </div>
              </div>
            </center>
          </form>
        </div>
      </div>
    </div>
    <!-- DOWNNLOADING MODAL -->
    <div id="downloadModal" class="modal hide fade" tabindex="-1" role="dialog" area-labelledby="downloadModalLabel" area-hidden="true">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" area-hidden="true"></button>
        <h3 id="myModalLabel">Sit back and relax.</h3>
      </div>
      <div class="modal-body">
        <p>
          Our Servers are powered by caffeinated hamsters, you won't be waiting long.
        </p>
        <div class="progress progress-striped progress-success active">
          <div id="progress_bar" class="bar"></div>
        </div>
      </div>
      <div class="modal-footer">
        <center>
          <button class="btn btn-inverse" data-dismiss="modal" area-hidden="true">Close</button>
        </center>
      </div>
    </div><!-- ABOUT MODAL -->
    <div id="myModal" class="modal hide fade" tabindex="-1" role="dialog" area-labelledby="myModalLabel" area-hidden="true">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" area-hidden="true"></button>
        <h3 id="myModalLabel">About &amp; FAQ</h3>
      </div>
      <div class="modal-body">
        <center>
          <img data-src="holder.js/260x180" alt="260x180" src="./img/bwdicon.png">
        </center>
        <h4>What Does This Site Do?</h4>
          After you select your a resolution and quantity, a custom script starts grabbing wallpapers from a wide range of sites, packages them up into a zip file and sends it to your downloads folder.<br />
        <h4>Is It Safe?</h4>
          It’s completely safe. The script just drops a zip file stocked with jpgs into your downloads folder.<br />
        <h4>Why Did You Make This?</h4>
          We both had some spare time over the summer and always enjoy taking on a new challenging project.<br />
        <h4>Why Don't You Have My Screen Size?</h4>
          Well not to say you're not special, but we can only put so many on the list. If you know your device's screen size find something close to it. If you don't know your size use <a target="_blank" href="http://www.whatismyscreenresolution.com/">this site</a> to get your resolution.<br />
        <h4>Can I See The Script?</h4>
          Sure. There's a tutorial on how to use the script on its own. However it is still only available for Mac OS and will require you to install and operate it through command line.<br />
        <a class="btn btn-info" target="_blank" href="http://www.instructables.com/id/Easy-Mac-Wallpaper-Downloader/">View Tutorial</a>
        <br>
        <hr>
        <h4>The Two Guys With Spare Time</h4>
        <div class="media">
          <a class="pull-left" href="#"><img src="./img/zackbama.png" alt="txtcla55_logo" width="64" height="64"></a>
          <div class="media-body">
            <h4 class="media-heading">
              Zach J.
            </h4>
            <p>
              I am a copywriter and geek with wide variety of interests many of which require a computer. If I’m not online (which is rare), I’ll be face deep in a book. My duty here was to make the pretty html and fill in any blank space with copy about the site. Visit my <a target="_blank" href="http://zachjordan.no-ip.org/">personal page</a> for more information.
            </p>
          </div>
        </div>
        <div class="media">
          <a class="pull-left" href="#"><img class="media-object" data-src="holder.js/64x64" alt="64x64" style="width: 64px; height: 64px;" src="./img/gnu.png"></a>
          <div class="media-body">
            <h4 class="media-heading">
              GNU-USER
            </h4>
            <p>
              Student by day, hacker by night. I can be found coding interesting projects in my spare time and doing academic research, I have a keen interest in all things technology and the hacker culture, with a focus on security and cryptography. To find out more, please see my <a target="_blank" href="https://github.com/gnu-user">github page</a> and follow me. Even better contribute to projects I am working on. I can always use more help!
            </p>
          </div>
        </div>
      </div>
      <div class="modal-footer">
        <center>
          <button class="btn btn-inverse" data-dismiss="modal" area-hidden="true">Close</button>
        </center>
      </div>
    </div><!-- END ABOUT MODAL-->