# Pepper_robot_ROS
Instruction on using ROS to communicate with pepper robot.
## OS and ROS Version
OS: Ubuntu 18.04

ROS: Melodic
## Chorepraphe
This is the official pepper software.

Download ```choregraphe-suite-2.5.10.7-linux64-setup.run``` by attached link
```
https://www.aldebaran.com/en/support/pepper-naoqi-2-9/downloads-softwares/former-versions?os=49&category=98
```

Run
```
chmod +x choregraphe-suite-2.5.10.7-linux64-setup.run
sudo ./choregraphe-suite-2.5.10.7-linux64-setup.run
```
Try to run the Chorepraphe
```
"/opt/Softbank Robotics/Choregraphe Suite 2.5/bin/choregraphe_launcher"
```
If the error shown in the terminal is ```/opt/Softbank Robotics/Choregraphe Suite 2.5/bin/../lib/../lib/../lib/libz.so.1: version `ZLIB_1.2.9' not found (required by /usr/lib/x86_64-linux-gnu/libpng16.so.16)```

Run
```
cd "/opt/Softbank Robotics/Choregraphe Suite 2.5/lib/"
sudo mv libz.so.1 libz.so.1.old
sudo ln -s /lib/x86_64-linux-gnu/libz.so.1
```
Now you can use the pre-programmed block in Chorepraphe to control the pepper robot.

## Python SDK
This part will explain how to control the pepper robot with Python.
Check the Python version and make sure it is ```Python 2.7```.
Install ```python2-dev```
```
sudo apt install python2-dev
```
Download ```pynaoqi-python2.7-2.5.7.1-linux64.tar.gz``` by attached link
```
https://www.aldebaran.com/en/support/pepper-naoqi-2-9/downloads-softwares/former-versions?os=49&category=108
```
Select ```2.5.10``` for ```Python 2.7 SDK```
