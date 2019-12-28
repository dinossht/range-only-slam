#!/usr/bin/env python

import nxt.locator
from nxt.motor import *
from nxt.sensor import *
import rospy
from std_msgs.msg import String,Int32


# init brick, see config file ~/.nxt-python
b = nxt.locator.find_one_brick()

# initialize motors
m_left = Motor(b, PORT_B)
m_right = Motor(b, PORT_C)


prev_ultra_data = 0
movavg_coef = 0.95

def talker():
    pub = rospy.Publisher('nxt_sensor_data', Int32, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(1)
    while not rospy.is_shutdown():
        data = \
            m_right.get_tacho().tacho_count#Ultrasonic(b, PORT_4).get_sample()

        rospy.loginfo(data)
        pub.publish(data)
        m_right.turn(-100, 360)
        rate.sleep()


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
