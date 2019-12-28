#!/usr/bin/env python

import nxt.locator
from nxt.motor import *
from nxt.sensor import *
import rospy
from std_msgs.msg import String
import numpy as np


# init brick, see config file ~/.nxt-python
b = nxt.locator.find_one_brick()

# initialize motors
m_left = Motor(b, PORT_B)
m_right = Motor(b, PORT_C)
both = nxt.SynchronizedMotors(m_left, m_right, 0)
leftboth = nxt.SynchronizedMotors(m_left, m_right, 100)
rightboth = nxt.SynchronizedMotors(m_right, m_left, 100)


mot_pow = 70
turnrad = 230/3
off_l = m_left.get_tacho().tacho_count
off_r = m_right.get_tacho().tacho_count

pub = rospy.Publisher('nxt_sensor_data', String, queue_size=10)

prevld = 0
prevrd = 0
tang = 0
def callback(data):
    global prevld, prevrd, tang
    # recieve data
    ch = data.data
    if ch == "w":
        print "Forwards"
        both.turn(mot_pow, 360, False)
    elif ch == "s":
        print "Backwards"
        both.turn(-mot_pow, 360, False)
    elif ch == "a":
        print "Left"
        leftboth.turn(mot_pow, turnrad, False)
    elif ch == "d":
        print "Right"
        rightboth.turn(mot_pow, turnrad, False)
    elif ch == "q":
        both.brake()


    # send data
    enc_l = m_left.get_tacho().tacho_count
    enc_r = m_right.get_tacho().tacho_count
    ultr = Ultrasonic(b, PORT_4).get_sample()

    ld = (enc_l - off_l) * 12 / 338
    rd = (enc_r - off_r) * 12 / 338

    tld = ld - prevld
    trd = rd - prevrd
    prevld = ld
    prevrd = rd

    if abs(tld+trd) >= 20:
        v = (tld+trd)/2
        ang = 0
    else:
        v = 0
        if abs(tld) > abs(trd):
            ang = 30 * np.sign(tld - trd) #* abs(tld) / abs(trd)
        else:
            ang = 30 * np.sign(tld-trd)#*abs(trd)/abs(tld)

    tang = (ang+tang) % 360

    data = \
        str(v) + " " + \
        str(tang) + " " + \
        str(ultr)
    pub.publish(data)


def nxt_node():
    rospy.init_node('listener', anonymous=True)
    sub = rospy.Subscriber("waypoint", String, callback, queue_size=1)
    rospy.spin()


if __name__ == '__main__':
    nxt_node()