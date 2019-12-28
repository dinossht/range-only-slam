#!/usr/bin/env python
import rospy
from std_msgs.msg import String


def callback(data):
    #rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    x = data.data.split()
    print(int(x[0]))
    print(int(x[1]))
    print(int(x[2]))

    #if int(x[0]) < 30:


def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("nxt_sensor_data", String, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


if __name__ == '__main__':
    listener()
