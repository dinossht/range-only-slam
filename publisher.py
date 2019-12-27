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


prev_ultra_data = 0
movavg_coef = 0.95


def talker():
    pub = rospy.Publisher('nxt_sensor_data', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        data = \
            str(m_left.get_tacho().tacho_count)+" "+\
            str(m_right.get_tacho().tacho_count)+" "+\
            str(Ultrasonic(b, PORT_4).get_sample())

        rospy.loginfo(data)
        pub.publish(data)
        rate.sleep()


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
