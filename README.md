# Pepper_Robot_ROS_Communication
Instruction on using ROS to communicate with pepper robot.
## OS, ROS Version, and Pepper Robot Version
OS: Ubuntu 18.04

ROS: Melodic

Pepper Robot:1.6
## Choregraphe
This is the official pepper software.

Download ```choregraphe-suite-2.5.10.7-linux64-setup.run``` by attached link
```
https://www.aldebaran.com/en/support/pepper-naoqi-2-9/downloads-softwares/former-versions?os=49&category=98
```
Select ```2.5.10 Setup```
Run
```
chmod +x choregraphe-suite-2.5.10.7-linux64-setup.run
```
```
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
```
```
sudo mv libz.so.1 libz.so.1.old
```
```
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
Select ```2.5.10 Python 2.7 SDK```

Run
```
cd /usr/local/lib/python2.7/dist-packages
```
```
sudo tar xvfz <where_the_package_is>/pynaoqi-python2.7-2.5.7.1-linux64.tar.gz
```
```
export PYTHONPATH=${PYTHONPATH}:/usr/local/lib/python2.7/dist-packages/pynaoqi-python2.7-2.5.7.1-linux64/lib/python2.7/site-packages
```
```
echo 'export PYTHONPATH=${PYTHONPATH}:/usr/local/lib/python2.7/dist-packages/pynaoqi-python2.7-2.5.7.1-linux64/lib/python2.7/site-packages' >> ~/.bashrc
```
For any errors, please check [troubleshooting](http://doc.aldebaran.com/2-5/dev/python/tips-and-tricks.html#python-sdk-troubleshooting).

Edit ```/usr/local/bin/qi*``` and change the first line from ```#!/usr/bin/python``` to ```#!/usr/bin/python2``` (If there are no any scripts show, run the next step to test if the naoqi install successfully. If yes, please ignore this step. Conversely, go to the error check step.)
```
sudo nano /usr/local/bin/qi*
```
Test if the naoqi install successfully
```
python2 -c 'from naoqi import ALProxy'
```
```
python2 -c 'import qi'
```
```
python2 -c 'import naoqi'
```
If something goes wrong, check that
```
python2 -c 'import sys;print "\n".join(sys.path)'
```
If it includes ```/usr/local/lib/python2.7/dist-packages/pynaoqi-python2.7-2.5.7.1-linux64/lib/python2.7/site-packages``` That means the current user has read access to the files and subdirectories in this directory. 

Run this command if the path already been added but the test is failed.
```
sudo chmod 755 /usr/local/lib/python2.7/dist-packages/pynaoqi-python2.7-2.5.7.1-linux64/lib/python2.7/site-packages/
```
Now, you can use **from naoqi import ALProxy** at the start of your ROS script and using the corresponding API in [here](http://doc.aldebaran.com/2-5/index_dev_guide.html) to control the pepper robot.

The above method of installing **Chorepraphe** and **Python SDK** from [here](https://nlp.fi.muni.cz/trac/pepper/wiki/InstallationInstructions).
## ROS Packages
Please copy all the packages under your ROS workspace and compile them. These ROS packages organised all the sensors on pepper robot and published as ROS topic. Before copying the packages, please check the dependencies.
### Dependencies
```
sudo apt-get install ros-melodic-octomap*
```
```
sudo apt-get install ros-melodic-camera-info-manager*
```
### Basic Configuration
```
sudo git clone https://github.com/ros-naoqi/pepper_robot.git
```
```
sudo apt-get install ros-melodic-pepper-meshes
```
```
sudo git clone https://github.com/ros-naoqi/libqi.git
```
```
sudo git clone https://github.com/ros-naoqi/libqicore.git
```

### Hardware Drivers and Simulation
Naoqi driver python
```
sudo git clone https://github.com/ros-naoqi/naoqi_bridge.git
```
### Run
Before running the launch file, please change the **type="state_publisher"** to **type="robot_state_publisher"** in the **pepper_publisher.launch**. Change **pepper_robot.xacro** to **pepper.urdf** in the **pepper_upload.launch**. Don't forget change the Ip address in the **pepper_full_py.launch** and the other launch files' Ip address shown in this file.
```
roscore
```
```
roslaunch pepper_bringup pepper_full_py.launch
```
If you might any error when running the **pepper_full_py.launch**, please check the message shown in terminal to install the missing package. The above code is a simple example to control the pepper robot by keyboard, it's also have the function of obstacle detection.

For more ROS packages, please check the ROS wiki of [pepper](https://wiki.ros.org/pepper).
