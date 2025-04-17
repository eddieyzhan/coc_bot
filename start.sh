#!/bin/bash

# Kill and restart adb
adb kill-server
adb start-server

# Run Python script
cd src
python3 main.py
