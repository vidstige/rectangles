#!/bin/sh
if [ ! -d venv/ ]; then
    python3 -m venv venv
    venv/bin/pip install -r requirements.txt
fi
convert input/1.png ppm:- | venv/bin/python3 main.py
