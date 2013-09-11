kinderbox
=========

A Jukebox for kids using RFID to select mp3 album


* * *


GPIO Usages
===========


UI Buttons:
-----------


__GPIO <==> Buttons__

* 23   -> Play/Pause (toggle)
* 22   -> Volume down
* 4    -> Volume up
* 18   -> Next
* 17   -> Prev


16x2 LCD:
-----------

__GPIO <==> LCD__
* 24   -> EN
* 25   -> RS
* 2    -> D4
* 3    -> D5
* 27   -> D6
* 7    -> D7




My Tasks
===========

Processing cover images:
-------------------------

Need a python script to do followings:

* scan all subfolders in /var/lib/mpd/music
* for all albums found do:
* read the barcode.id
* create a new folder in /var/www/images/{barcode id} (mkdir -p )
* create a symbolic link to the folder.jpg (sudo ln -s /var/lib/mpd/music/AceOfBase/Happy\ Nation\ \(1993\)/folder.jpg /var/www/images/{barcode id}/cover.jpg)




TODO
-----

* 16x2 LCD display for showing volume and Track
* Power management for Amplifyer and rPi
* Moving the UI (Play/Pause, Next, Prev, Volume UP, Volume DOWN, Display)
* Management module for adding new music album and matching with RFID codes  



