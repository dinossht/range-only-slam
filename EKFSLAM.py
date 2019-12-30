#!/usr/bin/env python

import numpy as np


Q = np.eye(3, dtype=int)


def xpred_f(x, u):
    # takes a pose and odometry and predicts it to the next time step
    x_pred = [0, 0, 0]
    x_pred[0] = x[0] + u[0] * np.cos(x[2])  # x pos
    x_pred[1] = x[1] + u[0] * np.sin(x[2])  # y pos
    x_pred[2] = (x[2] + u[2]) % (2 * np.pi)  # heading
    return x_pred


def Fx(x, u):
    return np.array([\
        [1, 0, -u[0] * np.sin(x[2])],\
        [0, 1, u[0] * np.cos(x[2])],\
        [0, 0, 1]])


def Fu(x, u):
    return np.array([\
        [np.cos(x[2]), 0, 0],\
        [np.sin(x[2]), 0, 0],\
        [0, 0, 1]])


def predict(x, P, zOdo):
    x_pred = xpred_f(x, zOdo)
    F_x = Fx(x, zOdo)
    F_u = Fu(x, zOdo)

    Ppred = F_x * P * F_x.transpose() + F_u * Q * F_u.transpose()

    return x_pred, Ppred

