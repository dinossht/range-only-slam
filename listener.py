#!/usr/bin/env python
import rospy
from std_msgs.msg import String, Int32
import numpy as np


# parameters
WHEEL_RAD = 2.16  # cm
WHEEL_DIST = 12.0  # mm
SONAR_ARM = 5  # cm  ultrasonic accuracy: +/- 3 cm, range [0 255]cm

tacho_off_l = 0
tacho_off_r = 0
prev_tacho_l = 0
prev_tacho_r = 0
SCALE = 1.0375
offset_calculated = False


def sonar_tf(raw_data):
    if raw_data >= 14 and raw_data <= 44:
        return -0.0094 * raw_data**2 + 1.6729 * raw_data - 19.7511
    else:
        return -1


pub = rospy.Publisher('slam_data', String, queue_size=1)
def callback(data):
    global offset_calculated, prev_tacho_l, prev_tacho_r, tacho_off_l, tacho_off_r, SCALE

    raw = data.data.split()
    # calculate velocity and angle
    # calculate tacho offset
    if offset_calculated == False:
        tacho_off_l = int(raw[0])
        tacho_off_r = int(raw[1])
        offset_calculated = True

    tacho_l = (int(raw[0]) - tacho_off_l) * 2 * np.pi * 2.16 / 360  # cm
    tacho_r = (int(raw[1]) - tacho_off_r) * 2 * np.pi * 2.16 / 360  # cm

    rel_tacho_l = tacho_l - prev_tacho_l
    rel_tacho_r = tacho_r - prev_tacho_r
    prev_tacho_l = tacho_l
    prev_tacho_r = tacho_r

    dist_u = (rel_tacho_l + rel_tacho_r) / 2

    # calculate angle
    ang = SCALE * (180 / np.pi) * (rel_tacho_r - rel_tacho_l) / WHEEL_DIST

    # calculate sonar
    sonar = sonar_tf(int(raw[2])) + SONAR_ARM  # cm

    print(dist_u, ang, sonar)
    # publish slam data
    data = \
        str(dist_u) + " " + \
        str(ang) + " " + \
        str(sonar)
    pub.publish(data)


def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("nxt_sensor_data", String, callback)
    rospy.spin()


if __name__ == '__main__':
    listener()
