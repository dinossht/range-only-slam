#!/usr/bin/env python

import nxt.locator
from nxt.motor import *
from nxt.sensor import *
import rospy
from std_msgs.msg import String
import numpy as np

# parameters
WHEEL_RAD = 21.6  # mm
WHEEL_DIST = 120  # mm
SONAR_ARM = 50  # mm

MOT_POW = 70  # [-128,127]
TURN_ANG = 45  # degrees
TURN_RAD = TURN_ANG * 2.8#(WHEEL_DIST / 2) / WHEEL_RAD

FORWARD_DIST = 50  # mm
FORWARD_ANG = FORWARD_DIST * 360 / (2*np.pi*WHEEL_RAD)

# init brick, see config file ~/.nxt-python to choose between bluetooth and usb
b = nxt.locator.find_one_brick()
print("Brick connected")

# initialize motors
m_left = Motor(b, PORT_B)
m_right = Motor(b, PORT_C)
both = nxt.SynchronizedMotors(m_left, m_right, 0)
leftboth = nxt.SynchronizedMotors(m_left, m_right, 100)
rightboth = nxt.SynchronizedMotors(m_right, m_left, 100)
print("Initialized motors")

pub = rospy.Publisher('nxt_sensor_data', String, queue_size=1)


def callback(data):
    # recieve waypoint
    ch = data.data
    if ch == "w":
        both.turn(MOT_POW, FORWARD_ANG, True)
    elif ch == "s":
        both.turn(-MOT_POW, FORWARD_ANG, True)
    elif ch == "a":
        leftboth.turn(MOT_POW, TURN_RAD, True)
    elif ch == "d":
        rightboth.turn(MOT_POW, TURN_RAD, True)
    elif ch == "q":
        both.brake()

    # publish sensor raw
    data = \
        str(m_left.get_tacho().tacho_count) + " " + \
        str(m_right.get_tacho().tacho_count) + " " + \
        str(Ultrasonic(b, PORT_4).get_sample())
    pub.publish(data)


def nxt_node():
    rospy.init_node('listener', anonymous=True)
    sub = rospy.Subscriber("waypoint", String, callback, queue_size=1)
    rospy.spin()


if __name__ == '__main__':
    nxt_node()
