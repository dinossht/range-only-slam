#!/usr/bin/env python
import rospy
from std_msgs.msg import String, Int32
import matplotlib.pyplot as plt
import numpy as np
import EKFSLAM

# parameters
MAP_SIZE = 1000
map2d = np.zeros((MAP_SIZE+1, MAP_SIZE+1))

x_0 = MAP_SIZE / 2
y_0 = MAP_SIZE / 2

WIN_SIZE = 50

# states
xpred = [x_0, y_0, 0, 0, 0]
Ppred = np.eye(3+2)


"""
map2d[my][mx] = 150
sonar = int(x[2])
if sonar >= 10 and sonar <= 80:
    tx = mx + round(sonar * np.sin(np.pi * int(x[1]) / 180))
    ty = my - round(sonar * np.cos(np.pi * int(x[1]) / 180))
    map2d[ty][tx] = 255


map2d[my][mx] = 0  # 100
"""

def plot_map():
    global xpred, map2d
    plt.style.use('classic')
    x_c = int(round(xpred[0]))
    y_c = MAP_SIZE - int(round(xpred[1]))
    map2d[x_c][y_c] = 150
    plt.imshow(map2d, cmap='gray')
    plt.ylim((x_c - WIN_SIZE, x_c + WIN_SIZE))
    plt.xlim((y_c - WIN_SIZE, y_c + WIN_SIZE))
    plt.pause(0.01)


def callback(data):
    global xpred, Ppred, prev_heading, heading

    # get data odometry
    raw = data.data.split()
    dist_u = float(raw[0])
    new_ang = np.pi * float(raw[1]) / 180
    zOdo = [dist_u, 0, new_ang]

    # get measurement data
    sonar = float(raw[2])

    #if sonar != -1:

    xhat = xpred
    Phat = Ppred


    [xpred, Ppred] = EKFSLAM.predict(xhat, Phat, zOdo)
    print((xpred))
    print(Ppred.round())
    plot_map()

def visualization():
    rospy.init_node('visualization', anonymous=True)
    rospy.Subscriber("slam_data", String, callback)
    rospy.spin()


if __name__ == '__main__':
    visualization()
