# coding=utf-8
import numpy as np

def signal_window(win_wide, data_pdp):
    after_window = []
    for data_pdp_i in data_pdp:
        after_window_i = []
        a = np.shape(data_pdp_i)[0]
        i = 1
        while i * win_wide <= a:
            after_window_i.append(np.sum(data_pdp_i[(i - 1) * int(win_wide) : int(win_wide) * i, :], axis=0) / win_wide)
            i += 1
        after_window.append(np.array(after_window_i))
    return after_window
