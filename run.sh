#!/bin/bash
cd /home/semiflex/Desktop/projects/coolscreen
git fetch origin master
git reset --hard origin/master
python3 main.py
