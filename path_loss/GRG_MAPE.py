# coding=utf-8
import numpy as np

def GRG_MAPE_AVRG(w, n):
    # AVRG均值化生成
    w_avg = (1 / n) * np.sum(w, axis = 0)
    if w_avg == 0:
        x = 0
    else:
        x = w / w_avg
    return x

def GRG_MAPE_delta(x1, x2):
    a = np.abs(x1 - x2)
    return a

def GRG_MAPE_R(delta_min, delta_max, e, x):
    a = (delta_min + e * delta_max) / (x + e * delta_max)
    return a

def GRG_MAPE_r1(x, n):
    a = np.sum(x, axis = 0) / n
    return a

def pearson_fun(x, y, n):
    p = (n * np.sum(x * y) - np.sum(x) * np.sum(y)) / (np.sqrt( n * np.sum(x ** 2) - (np.sum(x)) ** 2) * np.sqrt(n * np.sum(y ** 2) - (np.sum(y)) ** 2))
    return p
