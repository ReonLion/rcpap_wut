# coding=utf-8

import numpy as np
from matplotlib import pyplot as plt
import timeit

from Dm_Drms_fun import Dm_Drms_fun

class rmsdop():
    def __init__(self):
        '''
        设置debug模式
        '''
        debug_mode = True
        
        dop_paras = np.load('../params/dop_paras.npz')
        dop_data_cache = np.load('../params/dop_data.npz')
        
        '''
        测试参数录入
        '''
        fc = dop_paras['fc']
        c = dop_paras['c']
        ATT = dop_paras['ATT']
        chirp_num = dop_paras['chirp_num']
        window = dop_paras['window']
        beg_p = dop_paras['beg_p']
        end_p = dop_paras['end_p']
        beg_t_mark = dop_paras['beg_t_mark']
        cable1 = dop_paras['cable1']
        cable2 = dop_paras['cable2']
        TX_power = dop_paras['TX_power']
        TX_Gain = dop_paras['TX_Gain']
        RX_Gain = dop_paras['RX_Gain']
        TX_heigh = dop_paras['TX_heigh']
        RX_heigh = dop_paras['RX_heigh']
        TIME = dop_paras['TIME']
        D_window = dop_paras['D_window']
        Hz_x = dop_paras['Hz_x']
        dop_data = dop_data_cache['for_dop']
        
        '''
        时延参数提取
        '''
        dop_window = []
        Thre = []
        num_a = np.shape(dop_data)[0]
        dop_window = dop_data.copy()
        lim_a = np.shape(dop_window)[0]
        
        ss_reg = []
        Dm = []
        Drms = []
        for i in range(0, lim_a):
            ss_reg.append(np.dot(np.abs(dop_window[i]), np.linalg.pinv(np.max(np.abs(dop_window[i]), axis = 0).reshape(1, -1))))
            Dm_cache, Drms_cache = Dm_Drms_fun(ss_reg[i], Hz_x)
            Dm.append(Dm_cache)
            Drms.append(Drms_cache)
            #ss_reg = []
        Dm = np.array(Dm)
        Drms = np.array(Drms)
        
        h1 = (np.max(Dm, axis=0) - np.min(Dm, axis=0)) / (1 + np.log2(Dm.shape[0]))
        
        
        '''
        debug message
        '''
        if debug_mode:
            print('dop_data')
            print(dop_data.shape)
            print(dop_data[0][0, 0:6])
            print(dop_data[30][0, 0:6])
            print(dop_data[-1][0, 0:6])
            print('Dm')
            print(Dm.shape)
            print(Dm[0:6])
            print(Dm[-6:])
            print('Drms')
            print(Drms.shape)
            print(Drms[0:6])
            print(Drms[-6:])

if __name__ == '__main__':
    begin_time = timeit.default_timer()
    
    rmsdop()
    
    end_time = timeit.default_timer()
    print('Running time')
    print(str(end_time - begin_time))
