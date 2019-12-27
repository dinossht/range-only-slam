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
    pub = rospy.Publisher('chatter', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        hello_str = str(m_left.get_tacho().tacho_count)#"hello world %s" % rospy.get_time()
        rospy.loginfo(hello_str)
        pub.publish(hello_str)
        rate.sleep()






"""

while True:
    # time loop
    t = time.time()

    # read data
    encoder_l = m_left.get_tacho().tacho_count
    encoder_r = m_right.get_tacho().tacho_count

    ultra_data = Ultrasonic(b, PORT_4).get_sample()
    prevval = ultra_data * movavg_coef + prev_ultra_data * (1-movavg_coef)

    # time loop  
    print((time.time()-t) * 1000)
"""
if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
