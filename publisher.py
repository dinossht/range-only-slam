#!/usr/bin/env python

import nxt.locator
from nxt.motor import *
from nxt.sensor import *
import rospy
from std_msgs.msg import String


# init brick, see config file ~/.nxt-python
b = nxt.locator.find_one_brick()

# initialize motors
m_left = Motor(b, PORT_B)
m_right = Motor(b, PORT_C)
both = nxt.SynchronizedMotors(m_left, m_right, 0)
leftboth = nxt.SynchronizedMotors(m_left, m_right, 100)
rightboth = nxt.SynchronizedMotors(m_right, m_left, 100)

p = 75
def send_motor_setpoint(data):
    global both, leftboth, rightboth
    ch = data.data
    if ch == "w":
        print "Forwards"
        both.turn(p, 360, False)
    elif ch == "s":
        print "Backwards"
        both.turn(-p, 360, False)
    elif ch == "a":
        print "Left"
        leftboth.turn(p, 90, False)
    elif ch == "d":
        print "Right"
        rightboth.turn(p, 90, False)


count = 0
def talker():
    global count
    pub = rospy.Publisher('nxt_sensor_data', String, queue_size=10)
    sub = rospy.Subscriber("waypoint", String, send_motor_setpoint, queue_size=1)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(5)

    for i in range(10):
        rate.sleep()
    off_l = m_left.get_tacho().tacho_count
    off_r = m_right.get_tacho().tacho_count


    while not rospy.is_shutdown():
        count = count + 1
        enc_l = m_left.get_tacho().tacho_count
        enc_r = m_right.get_tacho().tacho_count
        ultr = Ultrasonic(b, PORT_4).get_sample()
        data = \
            str(enc_l-off_l)+" "+\
            str(enc_r-off_r)+" "+\
            str(ultr)

        rospy.loginfo(data)
        #if count % 10 == 0:
        sub = rospy.Subscriber("waypoint", String, send_motor_setpoint)

        pub.publish(data)
        rate.sleep()


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
