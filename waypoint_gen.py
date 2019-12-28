#!/usr/bin/env python

import rospy
from std_msgs.msg import String

def waypoint_talker():
    pub = rospy.Publisher('waypoint', String, queue_size=10)
    rospy.init_node('waypoint_talker', anonymous=True)
    rate = rospy.Rate(1)
    while not rospy.is_shutdown():
        data = "a"
        rospy.loginfo(data)
        pub.publish(data)
        rate.sleep()



if __name__ == '__main__':
    try:
        waypoint_talker()
    except rospy.ROSInterruptException:
        pass
