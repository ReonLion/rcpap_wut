# coding=utf-8
import numpy as np

def GPS_2_distance(GPS_rx, GPS_tx):
    weidu_rx = GPS_rx[:, 0]
    jingdu_rx = GPS_rx[:, 1]
    weidu_tx = GPS_tx[:, 0]
    jingdu_tx = GPS_tx[:, 1]

    C = np.sin(weidu_rx * np.pi / 180) * np.sin(weidu_tx * np.pi / 180) + np.cos(weidu_rx * np.pi / 180) * np.cos(weidu_tx * np.pi / 180) * np.cos((jingdu_rx - jingdu_tx) * np.pi / 180)
    d = 6371.3 * np.arccos(C)
    
    return d