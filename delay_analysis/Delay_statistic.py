# coding=utf-8

import numpy as np
from matplotlib import pyplot as plt
import timeit

class Delay_statistic():
    def __init__(self):
        '''
        设置debug模式
        '''
        debug_mode = True
        
        '''
        rmsdelay_pathnum_analysis_main_function.py结果导入
        '''
        RMS_results = np.load('../params/RMS_results.npz')
        
        '''
        参数设置
        '''
        beg = 1
        end_p = 125
        
        '''
        数据读入
        '''
        Tm1 = RMS_results['TM']
        Trms1 = RMS_results['TRMS']
        num_path1 = RMS_results['num_path']
        X_axis1 = RMS_results['X_axis']
        TIME1 = RMS_results['TIME']
        
        Tm1 = Tm1[beg - 1 : end_p]
        Trms1 = Trms1[beg - 1 : end_p]
        num_path1 = num_path1[beg - 1 : end_p]
        X_axis1 = X_axis1[beg - 1 : end_p]
        TIME1 = TIME1[beg - 1 : end_p]
        
        Tm = Tm1.copy()
        Trms = Trms1.copy()
        print('Tm')
        print(Tm.shape)
        
        h1 = (np.max(Tm, axis=0) - np.min(Tm, axis=0)) / (1 + np.log2(np.shape(Tm)[0]))
        h2 = (np.max(Trms, axis=0) - np.min(Trms, axis=0)) / (1 + np.log2(np.shape(Trms)[0]))
        num1 = (np.max(Tm, axis=0) - np.min(Tm, axis=0)) / h1
        num2 = (np.max(Trms, axis=0) - np.min(Trms, axis=0)) / h2
        
        
        
        '''
        debug message
        '''
        if debug_mode:
            print('h1')
            print(h1)
            print('h2')
            print(h2)
            print('num1')
            print(num1)
            print('num2')
            print(num2)
        
        
if __name__ == '__main__':
    begin_time = timeit.default_timer()
    
    Delay_statistic()
    
    end_time = timeit.default_timer()
    print('Running time')
    print(str(end_time - begin_time))
