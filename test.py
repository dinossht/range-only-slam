#!/usr/bin/env python

import nxt.locator
from nxt.motor import *
from nxt.sensor import *

import matplotlib.pyplot as plt
from matplotlib import style

import time


# init brick, see config file ~/.nxt-python
b = nxt.locator.find_one_brick()


m_left = Motor(b, PORT_B)
m_right = Motor(b, PORT_C)

style.use('fivethirtyeight')

fig = plt.figure()
ax1 = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2)
prevval = 0
for i in range(1000):
	t = time.time()
	motorl = m_left.get_tacho().tacho_count
	#print(motorl)
	val = Ultrasonic(b, PORT_4).get_sample()
	prevval = val * 0.9 + prevval * 0.1;
	#print(prevval)

	ax1.scatter(i,prevval)
	ax1.set_ylim(0,85)
	ax1.set_xlim(i-100,i)

	ax2.scatter(i,motorl)
	ax2.set_xlim(i-100,i)
		

	plt.pause(0.0001)

	elapsed = time.time() - t
	print(elapsed*1000)

#print 'Touch:', Touch(b, PORT_1).get_sample()		
#print 'Sound:', Sound(b, PORT_2).get_sample()
#print 'Light:', Light(b, PORT_3).get_sample()
#print 'Ultrasonic:', Ultrasonic(b, PORT_4).get_sample()
