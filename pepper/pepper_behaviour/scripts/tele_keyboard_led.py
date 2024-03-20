#!/usr/bin/env python
import rospy
from naoqi import ALProxy
from std_msgs.msg import String
from sensor_msgs.msg import LaserScan, Range
import pygame
import time

pepper_id = "192.168.1.91"
pepper_port = 9559
motion_proxy = ALProxy("ALMotion", pepper_id, pepper_port)
led_proxy = ALProxy("ALLeds", pepper_id, pepper_port)
battery_proxy = ALProxy("ALBattery", pepper_id, pepper_port)

motion_proxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", False]])

names  = ['HeadYaw' ,'HeadPitch']
stiffnessLists  = 0.0
timeLists  = 1.0
motion_proxy.stiffnessInterpolation(names, stiffnessLists, timeLists)

class PepperMove():
    def __init__(self):
        rospy.init_node('pepper_move')
        self.move = String()
        self.sonar_front = Range()
        self.sonar_back = Range()
        self.laser_left = LaserScan()
        self.laser_right = LaserScan()
        self.laser_left_data = float('inf')
        self.laser_right_data = float('inf')
        self.sub_sonar_front = rospy.Subscriber('/pepper_robot/sonar/front/sonar', Range, self.callbackSonarFront)
        self.sub_sonar_back = rospy.Subscriber('/pepper_robot/sonar/back/sonar', Range, self.callbackSonarBack)
        self.sub_laser_left = rospy.Subscriber('/laser/srd_left/scan', LaserScan, self.callbackLaserLeft)
        self.sub_laser_right = rospy.Subscriber('/laser/srd_right/scan', LaserScan, self.callbackLaserRight)
        rospy.loginfo("Movement Node Started")
        self.rate = rospy.Rate(1)
        pygame.init()
        pygame.display.set_mode((1, 1))
        self.main()
    
    def callbackSonarFront(self, data):
        self.sonar_front = data.range

    def callbackSonarBack(self, data):
        self.sonar_back = data.range

    def callbackLaserLeft(self, data):
        self.laser_left = data.ranges
        self.laser_left_data = min(self.laser_left)
        
    def callbackLaserRight(self, data):
        self.laser_right = data.ranges
        self.laser_right_data = min(self.laser_right)

    def on_key_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.move = "forward"
                motion_proxy.move(0.1, 0, 0)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                self.move = "stop"
                motion_proxy.move(0, 0, 0)
                rospy.loginfo("Current Battery Level: %s%%" % battery_proxy.getBatteryCharge())
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                self.move = "back"
                motion_proxy.move(-0.1, 0, 0)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_s:
                self.move = "stop"
                motion_proxy.move(0, 0, 0)
                rospy.loginfo("Current Battery Level: %s%%" % battery_proxy.getBatteryCharge())
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.move = "left"
                motion_proxy.move(0, 0.1, 0)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                self.move = "stop"
                motion_proxy.move(0, 0, 0)
                rospy.loginfo("Current Battery Level: %s%%" % battery_proxy.getBatteryCharge())
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                self.move = "right"
                motion_proxy.move(0, -0.1, 0)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                self.move = "stop"
                motion_proxy.move(0, 0, 0)
                rospy.loginfo("Current Battery Level: %s%%" % battery_proxy.getBatteryCharge())
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                self.move = "lrotate"
                motion_proxy.move(0, 0, 0.2)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_q:
                self.move = "stop"
                motion_proxy.move(0, 0, 0)
                rospy.loginfo("Current Battery Level: %s%%" % battery_proxy.getBatteryCharge())
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                self.move = "rrotate"
                motion_proxy.move(0, 0, -0.2)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_e:
                self.move = "stop"
                motion_proxy.move(0, 0, 0)
                rospy.loginfo("Current Battery Level: %s%%" % battery_proxy.getBatteryCharge())
        
        rospy.loginfo("Publishing movement command: %s" % self.move)

    def main(self):
        while not rospy.is_shutdown():
            for event in pygame.event.get():
                if event.type in (pygame.KEYDOWN, pygame.KEYUP):
                    self.on_key_event(event)

            if self.move == "forward" and self.sonar_front <= 0.5:
                motion_proxy.move(0, 0, 0)
                self.move = "stop"
                rospy.loginfo("Front sonat distance is less than 0.5")
                led_proxy.fadeRGB("FaceLeds", 1.0, 0.0, 0.0, 0.25)
                time.sleep(0.25)
                led_proxy.fadeRGB("FaceLeds", 1.0, 1.0, 1.0, 0.25)
                time.sleep(0.25)
                led_proxy.fadeRGB("FaceLeds", 1.0, 0.0, 0.0, 0.25)
                time.sleep(0.25)
                led_proxy.fadeRGB("FaceLeds", 1.0, 1.0, 1.0, 0.25)
            elif self.move == "back" and self.sonar_back <= 0.5:
                motion_proxy.move(0, 0, 0)
                self.move = "stop"
                rospy.loginfo("Back sonar distance is less than 0.5")
                led_proxy.fadeRGB("ChestLeds", 1.0, 0.0, 0.0, 0.25)
                time.sleep(0.25)
                led_proxy.fadeRGB("ChestLeds", 1.0, 1.0, 1.0, 0.25)
                time.sleep(0.25)
                led_proxy.fadeRGB("ChestLeds", 1.0, 0.0, 0.0, 0.25)
                time.sleep(0.25)
                led_proxy.fadeRGB("ChestLeds", 1.0, 1.0, 1.0, 0.25)
            elif self.move == "left" and self.laser_left_data <= 0.5:
                motion_proxy.move(0, 0, 0)
                self.move = "stop"
                rospy.loginfo("Left laser distance is less than 0.5")
                led_proxy.fadeRGB("LeftEarLedsEven", 0.0, 0.0, 1.0, 0.25)
                led_proxy.fadeRGB("LeftEarLedsOdd", 0.0, 0.0, 0.0, 0.25)
                time.sleep(0.25)
                led_proxy.fadeRGB("LeftEarLedsEven", 0.0, 0.0, 0.0, 0.25)
                led_proxy.fadeRGB("LeftEarLedsOdd", 0.0, 0.0, 1.0, 0.25)
                time.sleep(0.25)
                led_proxy.fadeRGB("LeftEarLedsEven", 0.0, 0.0, 1.0, 0.25)
                led_proxy.fadeRGB("LeftEarLedsOdd", 0.0, 0.0, 0.0, 0.25)
                time.sleep(0.25)
                led_proxy.fadeRGB("LeftEarLedsEven", 0.0, 0.0, 1.0, 0.25)
                led_proxy.fadeRGB("LeftEarLedsOdd", 0.0, 0.0, 1.0, 0.25)
            elif self.move == "right" and self.laser_right_data <= 0.5:
                motion_proxy.move(0, 0, 0)
                self.move = "stop"
                rospy.loginfo("Right laser distance is less than 0.5")
                led_proxy.fadeRGB("RightEarLedsEven", 0.0, 0.0, 1.0, 0.25)
                led_proxy.fadeRGB("RightEarLedsOdd", 0.0, 0.0, 0.0, 0.25)
                time.sleep(0.25)
                led_proxy.fadeRGB("RightEarLedsEven", 0.0, 0.0, 0.0, 0.25)
                led_proxy.fadeRGB("RightEarLedsOdd", 0.0, 0.0, 1.0, 0.25)
                time.sleep(0.25)
                led_proxy.fadeRGB("RightEarLedsEven", 0.0, 0.0, 1.0, 0.25)
                led_proxy.fadeRGB("RightEarLedsOdd", 0.0, 0.0, 0.0, 0.25)
                time.sleep(0.25)
                led_proxy.fadeRGB("RightEarLedsEven", 0.0, 0.0, 1.0, 0.25)
                led_proxy.fadeRGB("RightEarLedsOdd", 0.0, 0.0, 1.0, 0.25)

            pygame.time.delay(1)
            self.rate.sleep()

if __name__ == '__main__':
    pepper_move = PepperMove()