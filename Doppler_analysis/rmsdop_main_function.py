# coding=utf-8

import numpy as np
from matplotlib import pyplot as plt
import timeit

from Doppler_analysis.Dm_Drms_fun import Dm_Drms_fun

class rmsdop():
    def __init__(self):
        '''
        设置debug模式
        '''
        debug_mode = False
        
        dop_paras = np.load('./params/dop_paras.npz')
        dop_data_cache = np.load('./params/dop_data.npz')
        
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
        h2 = (np.max(Drms, axis=0) - np.min(Drms, axis=0)) / (1 + np.log2(Drms.shape[0]))
        num1 = (np.max(Dm, axis=0) - np.min(Dm, axis=0)) / h1
        num2 = (np.max(Drms, axis=0) - np.min(Drms, axis=0)) / h2
        
        a1, b1_cache = np.histogram(Dm, int(np.ceil(num1)))
        b1 = []
        for i in range(0, b1_cache.shape[0] - 1):
            b1.append((b1_cache[i] + b1_cache[i + 1]) / 2)
        b1 = np.array(b1)
        
        a2, b2_cache = np.histogram(Drms, int(np.ceil(num2)))
        b2 = []
        for i in range(0, b2_cache.shape[0] - 1):
            b2.append((b2_cache[i] + b2_cache[i + 1]) / 2)
        b2 = np.array(b2)
        
        A1 = a1 / np.sum(a1, axis = 0)
        A2 = a2 / np.sum(a2, axis = 0)
        
        '''
        图形生成程序
        '''
        '''
        绘制保存fig3
        '''
        fig = plt.figure(tight_layout = True)
        ax = fig.add_subplot(111)
        
        ax.plot(TIME, Dm, 'b', linewidth = 2)
        
        ax.set_xlim(np.min(TIME), np.max(TIME))
        ax.set_ylim(np.min(Dm), np.max(Dm))
        ax.set_xlabel('Time in s', fontproperties = 'Times New Roman', fontsize = 10)
        ax.set_ylabel('Mean Doppler in Hz', fontproperties = 'Times New Roman', fontsize = 10)
        ax.grid(True)
        
        plt.savefig('./results/frequency_domain/rmsdop_main_function_fig3.png')
        plt.clf()
        # 保存此图变量
        np.savez('./plot_params/rmsdop_main_function_fig3.npz', TIME=TIME, Dm=Dm)
        
        '''
        绘制保存fig4
        '''
        fig = plt.figure(tight_layout = True)
        ax = fig.add_subplot(111)
    
        ax.plot(TIME, Drms, 'b', linewidth = 2)
    
        ax.set_xlim(np.min(TIME), np.max(TIME))
        ax.set_ylim(np.min(Drms), np.max(Drms))
        ax.set_xlabel('Time in s', fontproperties = 'Times New Roman', fontsize = 10)
        ax.set_ylabel('RMS Doppler in Hz', fontproperties = 'Times New Roman', fontsize = 10)
        ax.grid(True)
    
        plt.savefig('./results/frequency_domain/rmsdop_main_function_fig4.png')
        plt.clf()
        # 保存此图变量
        np.savez('./plot_params/rmsdop_main_function_fig4.npz', TIME=TIME, Drms=Drms)
        
        '''
        绘制保存fig6
        '''
        fig = plt.figure(tight_layout = True)
        ax = fig.add_subplot(111)
        
        Dm_sort = np.sort(Dm)
        count = Dm.shape[0]
        Dm_cdf = [[], []]
        for i in range(0, count):
            Dm_cdf[0].append(Dm_sort[i])
            Dm_cdf[1].append((i + 1) / count)
        
        ax.step(Dm_cdf[0], Dm_cdf[1], 'b', linewidth = 2.0)
        
        ax.set_xlabel('RMS Doppler in Hz', fontproperties = 'Times New Roman', fontsize = 10)
        ax.set_ylabel('CDF of mean Doppler', fontproperties = 'Times New Roman', fontsize = 10)
        ax.grid(True)
    
        plt.savefig('./results/frequency_domain/rmsdop_main_function_fig6.png')
        plt.clf()
        # 保存此图变量
        np.savez('./plot_params/rmsdop_main_function_fig6.npz', Dm=Dm)
        
        '''
        绘制保存fig8
        '''
        fig = plt.figure(tight_layout = True)
        ax = fig.add_subplot(111)
        
        Drms_sort = np.sort(Drms)
        count = Drms.shape[0]
        Drms_cdf = [[], []]
        for i in range(0, count):
            Drms_cdf[0].append(Drms_sort[i])
            Drms_cdf[1].append((i + 1) / count)
        
        ax.step(Drms_cdf[0], Drms_cdf[1], 'b', linewidth = 2.0)
        
        ax.set_xlabel('RMS Doppler in Hz', fontproperties = 'Times New Roman', fontsize = 10)
        ax.set_ylabel('CDF of RMS Doppler', fontproperties = 'Times New Roman', fontsize = 10)
        ax.grid(True)
    
        plt.savefig('./results/frequency_domain/rmsdop_main_function_fig8.png')
        plt.clf()
        # 保存此图变量
        np.savez('./plot_params/rmsdop_main_function_fig8.npz', Drms=Drms)
        
        '''
        绘制保存fig9
        '''
        fig = plt.figure(tight_layout = True)
        ax = fig.add_subplot(111)
    
        ax.bar(b1, A1, color = 'b', width = 6)
        
        ax.set_xlabel('Mean Doppler in Hz', fontproperties = 'Times New Roman', fontsize = 10)
        ax.set_ylabel('PDF of mean Doppler', fontproperties = 'Times New Roman', fontsize = 10)
        ax.grid(True)
    
        plt.savefig('./results/frequency_domain/rmsdop_main_function_fig9.png')
        plt.clf()
        # 保存此图变量
        np.savez('./plot_params/rmsdop_main_function_fig9.npz', b1=b1, A1=A1)
        
        '''
        绘制保存fig10
        '''
        fig = plt.figure(tight_layout = True)
        ax = fig.add_subplot(111)
    
        ax.bar(b2, A2, color = 'b', width = 6)
    
        ax.set_xlabel('RMS Doppler in Hz', fontproperties = 'Times New Roman', fontsize = 10)
        ax.set_ylabel('PDF of RMS Doppler', fontproperties = 'Times New Roman', fontsize = 10)
        ax.grid(True)
    
        plt.savefig('./results/frequency_domain/rmsdop_main_function_fig10.png')
        plt.clf()
        # 保存此图变量
        np.savez('./plot_params/rmsdop_main_function_fig10.npz', b2=b2, A2=A2)
        
        plt.close('all')
        
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
            print('h1, h2, num1, num2')
            print(h1, h2, num1, num2)
            print('A1')
            print(A1)
            print('b1')
            print(b1)
            print('A2')
            print(A2)
            print('b2')
            print(b2)
            
            

if __name__ == '__main__':
    begin_time = timeit.default_timer()
    
    rmsdop()
    
    end_time = timeit.default_timer()
    print('Running time')
    print(str(end_time - begin_time))
