#!/usr/bin/env python
import rospy
from std_msgs.msg import String, Int32
import numpy as np
import matplotlib.pyplot as plt


s = 100
map2d = np.zeros((s+1, s+1))
x_off = s/2
y_off = s/2
mx = x_off
my = y_off

pub = rospy.Publisher('ultrasound', Int32, queue_size=10)
def callback(data):
    global mx, my
    x = data.data.split()
    print(int(x[0]))
    print(int(x[1]))
    print(int(x[2]))
    print("        ")
    pub.publish(int(x[2]))

    mx = mx + round(int(x[0]) * np.sin(np.pi * int(x[1]) / 180))
    my = my + round(int(x[0]) * np.cos(np.pi * int(x[1]) / 180))

    print(mx)
    print(my)
    print("        ")
    map2d[mx][my] = 1
    plt.imshow(map2d)
    plt.gcf().set_facecolor("white")
    plt.pause(0.1)
    #if int(x[0]) < 30:


def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("nxt_sensor_data", String, callback)
    rospy.spin()


if __name__ == '__main__':
    listener()
