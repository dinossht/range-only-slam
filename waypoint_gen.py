#!/usr/bin/env python

import rospy
from std_msgs.msg import String
import sys
import tty, termios


def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def waypoint_talker():
    pub = rospy.Publisher('waypoint', String, queue_size=1)
    rospy.init_node('waypoint_talker', anonymous=True)
    rate = rospy.Rate(5)
    while not rospy.is_shutdown():
        data = getch()
        rospy.loginfo(data)
        pub.publish(data)
        rate.sleep()


if __name__ == '__main__':
    try:
        waypoint_talker()
    except rospy.ROSInterruptException:
        pass
