kinderbox
=========

A Jukebox for kids using RFID to select mp3 album


GPIO Usages
************

UI Buttons:
-----------

GPIO <==> Buttons
23   -> Play/Pause (toggle)
22   -> Volume down
4    -> Volume up
18   -> Next
17   -> Prev


16x2 LCD:
-----------

GPIO <==> LCD
24   -> EN
25   -> RS
2    -> D4
3    -> D5
27   -> D6
7    -> D7






TODO

- 16x2 LCD display for showing volume and Track
- Power management for Amplifyer and rPi
- Moving the UI (Play/Pause, Next, Prev, Volume UP, Volume DOWN, Display)
- Management module for adding new music album and matching with RFID codes  
