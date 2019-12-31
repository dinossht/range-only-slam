#!/usr/bin/env python

import numpy as np


Q = np.eye(3, dtype=int)


def f(x, u):
    # takes a pose and odometry and predicts it to the next time step
    x_pred = [0, 0, 0]
    x_pred[2] = (x[2] + u[2]) % (2 * np.pi)  # heading
    x_pred[0] = x[0] + u[0] * np.cos(x_pred[2])  # x pos
    x_pred[1] = x[1] + u[0] * np.sin(x_pred[2])  # y pos

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


def predict(eta, P, zOdo):
    l = len(eta)
    x = eta[0:3]  # pose

    xpred = f(x, zOdo)
    F_x = Fx(x, zOdo)
    F_u = Fu(x, zOdo)

    Ppred = np.zeros([l, l])
    Ppred[0:3, 0:3] = F_x.dot(P[0:3, 0:3]).dot(F_x.transpose()) + F_u.dot(Q).dot(F_u.transpose())

    m = []
    if l > 3:
        m = eta[3:l]  # map

        Ppred[0:3, 3:l] = F_x.dot(P[0:3, 3:l])
        Ppred[3:l, 0:3] = Ppred[0:3, 3:l].transpose()

    # concatenate pose and landmarks again
    etapred = xpred + m

    return etapred, Ppred

