#!/bin/bash

sudo stty -F /dev/ttyUSB0 115200 cs8 ignbrk -brkint -icrnl -imaxbel -opost -onlcr -isig -icanon -iexten -echo -echoe -echok -echoctl -echoke noflsh -ixon -crtscts
echo "0 0 0 0" > ${1}.txt
python pintadata.py ${1}.txt &
sudo cat /dev/ttyUSB0 | tee ${1}.txt
