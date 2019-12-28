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


prev_ultra_data = 0
movavg_coef = 0.95
ch = []


def callback(data):
    global both, leftboth, rightboth
    #rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    ch = data.data
    print(ch)
    if ch == "w":
        print
        "Forwards"
        both.turn(100, 360, False)
    elif ch == "s":
        print
        "Backwards"
        both.turn(-100, 360, False)
    elif ch == "a":
        print
        "Left"
        leftboth.turn(100, 90, False)
    elif ch == "d":
        print
        "Right"
        rightboth.turn(100, 90, False)

count = 0
def talker():
    global count
    pub = rospy.Publisher('nxt_sensor_data', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)

    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        count = count + 1

        data = \
            str(m_left.get_tacho().tacho_count)+" "+\
            str(m_right.get_tacho().tacho_count)+" "+\
            str(Ultrasonic(b, PORT_4).get_sample())

        rospy.loginfo(data)
        if count % 10 == 0:
            sub = rospy.Subscriber("waypoint", String, callback)

        pub.publish(data)
        rate.sleep()


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
