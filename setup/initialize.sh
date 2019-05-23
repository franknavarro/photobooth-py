#!/bin/sh

#update packages already installed
sudo apt-get update

continue_key () {
  echo ""
  echo "Now installing $1"
  # read -rsn 1 -p "Press any key to continue" answer </dev/tty
}


#install dependencies
continue_key "python"
sudo apt-get install python python3 -y
continue_key "pygame"
sudo apt-get install python-pygame python3-pygame -y
continue_key "picamera"
sudo apt-get install python-picamera python3-picamera -y
continue_key "rpi.gpio"
sudo apt-get install python-rpi.gpio python3-rpi.gpio -y

#Cups set up
continue_key "cups"
sudo apt-get install cups -y
sudo apt-get install python-cups python3-cups -y
sudo usermod -a -G lpadmin pi
sudo cp ~/photoboothdiy/setup/cupsd.conf /etc/cups/
sudo /etc/init.d/cups restart


#Download Pillow and its dependencies
continue_key "pillow"
sudo apt-get install libjpeg-dev -y
sudo apt-get install zlib1g-dev -y
sudo apt-get install libfreetype6-dev -y
sudo apt-get install liblcms2-dev -y
sudo apt-get install libopenjp2-7 -y
sudo apt-get install libtiff5 -y

sudo apt-get install python-pip python3-pip -y
sudo-apt get install python3-pil python3-imagetk

pip install Pillow
pip3 install Pillow
