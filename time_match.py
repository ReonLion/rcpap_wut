# coding=utf-8
import numpy as np

def time_match(after_window, T):
    time = []
    i = 0
    for i in range(0, len(after_window) - 1):
        a = np.shape(after_window[i])[0]
        time.append(np.linspace(T[i], T[i + 1], a))
    return time    
