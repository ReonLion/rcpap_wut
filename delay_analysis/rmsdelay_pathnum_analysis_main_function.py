# coding=utf-8

import numpy as np
from matplotlib import pyplot as plt
import timeit

from delay_analysis.Tm_Trms_fun import Tm_Trms_fun

class rmsdelay_pathnum_analysis():
    def __init__(self):
        '''
        设置debug模式
        '''
        debug_mode = True
    
        delay_paras = np.load('./params/delay_paras.npz')
        delay_data_cache = np.load('./params/delay_data.npz')
        
        '''
        测试参数录入
        '''
        fc = delay_paras['fc']
        c = delay_paras['c']
        ATT = delay_paras['ATT']
        chirp_num = delay_paras['chirp_num']
        window = delay_paras['window']
        beg_p = delay_paras['beg_p']
        end_p = delay_paras['end_p']
        beg_t_mark = delay_paras['beg_t_mark']
        cable1 = delay_paras['cable1']
        cable2 = delay_paras['cable2']
        TX_power = delay_paras['TX_power']
        TX_Gain = delay_paras['TX_Gain']
        RX_Gain = delay_paras['RX_Gain']
        TX_heigh = delay_paras['TX_heigh']
        RX_heigh = delay_paras['RX_heigh']
        TIME = delay_paras['TIME']
        TIME = TIME - 1
        D_window = delay_paras['D_window']
        delay_data = delay_data_cache['after_window']
        
        '''
        时延参数提取
        '''
        pdp_window = delay_data[0].copy()
        Thre = []
        num_a = delay_data.shape[0]
        for n in range(1, num_a - 1):
            num_thre = delay_data.shape[1]
            num_thre_b = delay_data.shape[2]
            pdp_window = np.vstack((pdp_window, delay_data[n]))
        pdp_window[:, 0] = pdp_window[:, 1]
        lim_a = pdp_window.shape[0]
        
        ss_reg_m = []
        Tm = []
        Trms = []
        index_final = []
        for i in range(0, lim_a):
            ss_reg = np.abs(pdp_window[i, :]) / np.max(np.abs(pdp_window[i, :]), axis=0)
            ss_reg_m.append(ss_reg)
            Thre_n = np.max(10 * np.log10(ss_reg_m[i][1499:2400]), axis=0) + 6
            Tm_cache, Trms_cahce, index_final_cache = Tm_Trms_fun(ss_reg, Thre_n)
            Tm.append(Tm_cache)
            Trms.append(Trms_cahce)
            index_final.append(index_final_cache)
            ss_reg = []
        ss_reg_m = np.array(ss_reg_m)
        Tm = np.array(Tm)
        Trms = np.array(Trms)
        
        path_num = []
        for j in range(0, lim_a):
            path_num.append(index_final[j].shape[0])
        path_num = np.array(path_num)
        
        '''
        图形生成程序
        '''
        
        '''
        绘制保存fig1
        '''
        fig = plt.figure(tight_layout = True)
        ax = fig.add_subplot(111)
        ax.plot(TIME, path_num, 'b')
        ax.grid(True)
        plt.savefig('./results/delay_domain/rmsdelay_pathnum_analysis_main_function_fig1.png')
        plt.clf()
        # 保存此图变量
        np.savez('./plot_params/rmsdelay_pathnum_analysis_main_function_fig1.npz', X=TIME, Y=path_num)
        
        '''
        绘制保存fig2
        '''
        fig = plt.figure(tight_layout = True)
        ax = fig.add_subplot(111)
        ax.plot(D_window, path_num, 'b')
        ax.grid(True)
        plt.savefig('./results/delay_domain/rmsdelay_pathnum_analysis_main_function_fig2.png')
        plt.clf()
        # 保存此图变量
        np.savez('./plot_params/rmsdelay_pathnum_analysis_main_function_fig2.npz', X=D_window, Y=path_num)
        
        '''
        绘制保存fig3
        '''
        fig = plt.figure(tight_layout = True)
        ax = fig.add_subplot(111)
        ax.plot(D_window, Trms, 'b')
        ax.grid(True)
        plt.savefig('./results/delay_domain/rmsdelay_pathnum_analysis_main_function_fig3.png')
        plt.clf()
        # 保存此图变量
        np.savez('./plot_params/rmsdelay_pathnum_analysis_main_function_fig3.npz', X=D_window, Y=Trms)
        
        '''
        绘制保存fig4
        '''
        fig = plt.figure(tight_layout = True)
        ax = fig.add_subplot(111)
        ax.plot(TIME, Trms, 'b')
        ax.grid(True)
        plt.savefig('./results/delay_domain/rmsdelay_pathnum_analysis_main_function_fig4.png')
        plt.clf()
        # 保存此图变量
        np.savez('./plot_params/rmsdelay_pathnum_analysis_main_function_fig4.npz', X=TIME, Y=Trms)
        
        plt.close('all')
        
        '''
        保存变量，供Delay_statisti使用
        '''
        #TIME = TIME
        #TM = Tm
        #TRMS = Trms
        #num_path = path_num
        #X_axis = D_window
        
        #np.savez('./params/RMS_results.npz', TIME = TIME, TM = Tm, TRMS = Trms, num_path = path_num, X_axis = D_window)
        
        '''
        debug message
        '''
        if debug_mode:
            print('D_window')
            print(D_window.shape)
            print('delay_data')
            print(delay_data.shape)
            print(delay_data[0][0, 0:6])
            print(delay_data[0][-1, 0:6])
            print(delay_data[-1][0, 0:6])
            print(delay_data[-1][-1, 0:6])
            print('pdp_window')
            print(pdp_window.shape)
            print(pdp_window[0, 0:6])
            print(pdp_window[-1, 0:6])
            print('ss_reg_m')
            print(ss_reg_m.shape)
            print(ss_reg_m[0, 0:6])
            print(ss_reg_m[-1, 0:6])
            print('Thre_n')
            print(Thre_n)
            print('Tm')
            print(Tm.shape)
            print(Tm[0:6])
            print(Tm[-6:])
            print('Trms')
            print(Trms.shape)
            print(Trms[0:6])
            print(Trms[-6:])
            print('path_num')
            print(path_num.shape)
            print(path_num[0:10])
            print(path_num[-10:])
    
if __name__ == '__main__':
    begin_time = timeit.default_timer()
    
    rmsdelay_pathnum_analysis()
    
    end_time = timeit.default_timer()
    print('Running time')
    print(str(end_time - begin_time))
