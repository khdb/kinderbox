#!/bin/bash
find /var/lib/mpd/music  -type d -maxdepth 1 -mindepth 1 -exec python createkinderboxalbum.py {} \;

