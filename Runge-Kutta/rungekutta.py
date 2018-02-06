#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt

def runge_kutta(f, a, b, N, init):
    h = (b - a) / N
    t = a
    w = init

    integral = np.array([[t, w]])

    for i in range(1,N+1):
        k1 = h * f(t, w)
        k2 = h * f(t + h/2, w + k1/2)
        k3 = h * f(t + h/2, w + k2/2)
        k4 = h * f(t + h, w + k3)

        w = w + (k1 + 2*k2 +2*k3 + k4) / 6
        t = a + i*h
        integral = np.append(integral, [[t, w]], axis=0)

    return integral

