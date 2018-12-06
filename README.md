# OpenMV Apriltag recognition

[![Build Status](https://travis-ci.org/Windesheim-Willy/openmv_apriltag.svg?branch=master)](https://travis-ci.org/Windesheim-Willy/openmv_apriltag)

The OpenMV apriltag component is being used to identify an apriltag ID and the orientation 

For more information, check out the wiki about the OpenMV Apriltag [Wiki](https://windesheim-willy.github.io/WillyWiki/Components/openmv_apriltag.html)

When first install:

--Add USB to static name (https://msadowski.github.io/linux-static-port/)
sudo nano /etc/udev/rules.d/99-usb-serial.rules

KERNEL=="ttyACM*", KERNELS=="1-1.1.2:1.0", SYMLINK+="sensor_openmv"

udevadm control --reload-rules

