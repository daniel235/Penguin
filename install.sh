#!/bin/bash

#install minimap2
git clone https://github.com/lh3/minimap2

#install squiggleKit & scrappie
git clone https://github.com/Psy-Fer/SquiggleKit.git
pip install numpy h5py sklearn matplotlib
pip install scrappie
pip3 install tensorflow==2.1.0
pip install keras
#create empty directory for data
mkdir Data/basecall/

#change permissions for folder
cd ..
chmod -R 777 Penguin
cd Penguin

#installing nanopolish
git clone --recursive https://github.com/jts/nanopolish.git
cd nanopolish
make

#install prerequisites for samtools
git clone https://github.com/samtools/htslib
cd htslib
autoheader
autoconf
./configure
make
make install

#install samtools
cd ..
git clone https://github.com/samtools/samtools
cd samtools
autoconf -Wno-syntax
./configure --without-curses
make
make install
cd ..
