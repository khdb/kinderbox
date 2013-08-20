#!/bin/bash
find . -type d -maxdepth 1 -mindepth 1 -exec createKinderBoxAlbum.py {} \;

