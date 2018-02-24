# coding=utf-8
import numpy as np

def distance_match(after_window, Dis):
    distance = []
    for i in range(0, len(after_window) - 1):
        a = np.shape(after_window[i])[0]
        distance.append(np.linspace(Dis[i], Dis[i + 1], a))
    return distance