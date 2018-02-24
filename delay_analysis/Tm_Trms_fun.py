# coding=utf-8

import numpy as np

from delay_analysis.path_selection_diff_fun import path_selection_diff_fun

def Tm_Trms_fun(ss_reg, Thre_n):
    index_final = path_selection_diff_fun(ss_reg, Thre_n)
    APDP = ss_reg.copy()
    APDP[int(APDP.shape[0]) - 50 - 1 : APDP.shape[0]] = 0
    
    for i in np.where(APDP < 10 ** (Thre_n / 10))[0].flat:
        APDP[i] = 0
    Apdp = APDP.copy()
    cloumn_average = Apdp.copy()
    Pm = np.sum(cloumn_average, axis = 0)
    Tm_cache = np.arange(10, 10 * cloumn_average.shape[0] + 10 / 1e9, 10)
    Tm = np.sum(Tm_cache * cloumn_average, axis=0) / Pm
    Trms_cache = (np.arange(10, 10 * cloumn_average.shape[0] + 10 / 1e9, 10) ** 2) * cloumn_average
    Trms = np.sqrt(np.sum(Trms_cache, axis=0) / Pm - Tm ** 2)
    
    return Tm, Trms, index_final
