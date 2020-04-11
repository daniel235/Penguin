#!/bin/bash

#install minimap2
git clone https://github.com/lh3/minimap2

#install squiggleKit & scrappie
git clone https://github.com/Psy-Fer/SquiggleKit.git
pip install numpy h5py sklearn matplotlib
pip install scrappie
pip3 install --user --upgrade tensorflow 
pip install keras
#create empty directory for data
mkdir Data/basecall/
