#!/usr/bin/env python

import nxt.locator
from nxt.motor import *
import time

def spin_around(b):
    m_left = Motor(b, PORT_B)
    m_left.turn(100, 360)
    m_right = Motor(b, PORT_C)
    m_right.turn(-100, 360)

b = nxt.locator.find_one_brick()
while True:
    spin_around(b)
    time.sleep(1)

