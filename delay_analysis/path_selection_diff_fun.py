# coding=utf-8

import numpy as np

def path_selection_diff_fun(ss_reg, Thre_n):
    signal_nor = ss_reg.copy()
    ss_data = 10 * np.log10(signal_nor)
    b = (np.where(ss_data < Thre_n))[0]
    for i in b.flat:
        ss_reg[i] = 0
    ss_data = ss_reg.copy()
    fst_diff = np.diff(ss_data)
    
    snd_diff = [0]
    for n in range(1, fst_diff.shape[0] - 1):
        if fst_diff[n] * fst_diff[n + 1] > 0:
            if fst_diff[n] > 0:
                fst_diff[n] = fst_diff[n - 1]
            elif fst_diff[n] < 0:
                fst_diff[n] = fst_diff[n + 1]
        #------------------------------------
        snd_diff.append(fst_diff[n] - fst_diff[n + 1])
    snd_diff = np.array(snd_diff)
    value = np.where(snd_diff > 0)[0]
    path_index = value + 1 + 1
    return path_index
