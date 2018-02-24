# coding=utf-8
import numpy as np

def CIR_window(win_wide, CIR_1):
    after_window_cir = []
    for CIR_1_i in CIR_1:
        a = np.shape(CIR_1_i)[0]
        i = 1
        while i * win_wide <= a:
            after_window_cir.append(CIR_1_i[(i - 1) * int(win_wide) : int(win_wide) * i, :])
            i += 1
    return after_window_cir
