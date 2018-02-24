# coding=utf-8
import numpy as np

def speed_match(after_window, rel_speed):
    V_rel = []
    for i in range(0, len(after_window) - 1):
        a = np.shape(after_window[i])[0]
        V_rel.append(np.linspace(rel_speed[i], rel_speed[i + 1], a))
    return V_rel