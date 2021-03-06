#!/usr/bin/env python
import math
import rospy

from chassis import Chassis
from speed_sensor import SpeedSensors
from imibot_driver.msg import DiffSpeed


class DiffDriveControlHandler:
    servo_min = 800  # Min pulse length out of 4096
    servo_max = 4095  # Max pulse length out of 4096
    servo_scale = servo_max - servo_min

    def __init__(self, rospy):
        print 'Differential drive node initialization...'
        self.left_speed = 0
        self.right_speed = 0
        self.left_length = 0
        self.right_length = 0

        print 'Initialize Components...'
        self.chassis = Chassis()
        self.speed_measures = SpeedSensors(rospy)

        print 'Register control topic...'
        rospy.Subscriber("robot_mg", DiffSpeed, self.move)
        print 'Done !'

    def setSpeed(self):
        self.chassis.setLeftSpeed(int(self.left_length))
        self.chassis.setRightSpeed(int(self.right_length))

    def move(self, msg):
        self.left_speed = msg.left_speed
        self.right_speed = msg.right_speed
        #print self.left_speed, self.right_speed

        if self.left_speed == 0 and self.right_speed == 0:
            self.chassis.stop()
            self.speed_measures.stop_left_speed()
            self.speed_measures.stop_right_speed()
            #print 'stop'
        else:
            self.left_length = (self.servo_scale * (abs(self.left_speed) / 100)) + self.servo_min
            self.right_length = (self.servo_scale * (abs(self.right_speed) / 100)) + self.servo_min

            if self.left_speed > 0 and self.right_speed > 0:
                self.speed_measures.set_left_direction(1)
                self.speed_measures.set_right_direction(1)
                #print 'forward'
                self.chassis.forward()
                self.setSpeed()
            elif self.left_speed < 0 and self.right_speed > 0:
                self.speed_measures.set_left_direction(0)
                self.speed_measures.set_right_direction(1)
                #print 'left'
                self.chassis.turnLeft()
                self.setSpeed()
            elif self.left_speed > 0 and self.right_speed < 0:
                self.speed_measures.set_left_direction(1)
                self.speed_measures.set_right_direction(0)
                #print 'right'
                self.chassis.turnRight()
                self.setSpeed()
            elif self.left_speed < 0 and self.right_speed < 0:
                self.speed_measures.set_left_direction(0)
                self.speed_measures.set_right_direction(0)
                #print 'reverse'
                self.chassis.reverse()
                self.setSpeed()
