# coding=utf-8

import numpy as np

def Dm_Drms_fun_matlab(ss_reg, Hz_x):
    Adop = ss_reg.copy()
    cloumn_average = Adop.copy()
    Bm = np.sum(cloumn_average, axis = 0)
    Dm = np.sum(Hz_x * (cloumn_average.T), axis = 1) / Bm
    Drms = np.sqrt(np.sum((Hz_x ** 2) * cloumn_average.T, axis = 1) / Bm - Dm ** 2)
    return Dm, Drms

def Dm_Drms_fun(ss_reg, Hz_x):
    Adop = ss_reg.copy()
    cloumn_average = Adop.copy()
    cloumn_average = cloumn_average.flatten()
    Bm = np.sum(cloumn_average, axis = 0)
    Dm = np.sum(Hz_x * cloumn_average, axis = 0) / Bm
    Drms = np.sqrt(np.sum((Hz_x ** 2) * cloumn_average, axis = 0) / Bm - Dm ** 2)
    return Dm, Drms    
