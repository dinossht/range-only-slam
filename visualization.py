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
#x = x_0
#y = y_0
#heading = 0



"""

s = 500
map2d = np.zeros((s+1, s+1))
x_off = s/2W
y_off = s/2
mx = x_off
my = y_off

win = 50

mx = int(mx + round(int(x[0]) * np.sin(np.pi * int(x[1]) / 180)))
my = int(my - round(int(x[0]) * np.cos(np.pi * int(x[1]) / 180)))

map2d[my][mx] = 150
sonar = int(x[2])
if sonar >= 10 and sonar <= 80:
    tx = mx + round(sonar * np.sin(np.pi * int(x[1]) / 180))
    ty = my - round(sonar * np.cos(np.pi * int(x[1]) / 180))
    map2d[ty][tx] = 255


map2d[my][mx] = 0  # 100
"""




def plot_map(dist_u, heading, sonar):
    global x, y
    plt.style.use('classic')
    #x = x + dist_u
    #map2d[int(round(y))][int(round(x))] = 150
    plt.imshow(map2d, cmap='gray')
    plt.ylim((x_0 - WIN_SIZE, x_0 + WIN_SIZE))
    plt.xlim((y_0 - WIN_SIZE, y_0 + WIN_SIZE))
    plt.pause(0.01)


xpred = [x_0, y_0, 0]
Ppred = np.eye(3)

def callback(data):
    global xpred, Ppred, prev_heading, heading

    # get data odometry
    raw = data.data.split()
    dist_u = float(raw[0])
    new_ang = np.pi * float(raw[1]) / 180
    zOdo = [dist_u, 0, new_ang]

    # get measurement data
    sonar = float(raw[2])

    plot_map(dist_u, xpred[2], sonar)
    #if sonar != -1:

    xhat = xpred
    Phat = Ppred


    [xpred, Ppred] = EKFSLAM.predict(xhat, Phat, zOdo)


def visualization():
    rospy.init_node('visualization', anonymous=True)
    rospy.Subscriber("slam_data", String, callback)
    rospy.spin()


if __name__ == '__main__':
    visualization()