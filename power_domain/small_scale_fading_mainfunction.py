# coding=utf-8
import numpy as np
from statsmodels.nonparametric.smoothers_lowess import lowess
from matplotlib import pyplot as plt
import timeit

from power_domain.Meas_LCR_AFD import Meas_LCR_AFD

class small_scale_fading():
    def __init__(self, **kwargs):
        '''
        设置debug模式
        '''
        debug_mode = True
        
        ssf_paras = np.load('./params/ssf_paras.npz')
        ssf_data = np.load('./params/ssf_data.npz')
        
        '''
        测试参数录入
        '''
        fc = ssf_paras['fc'] / 1e9                                          # 载波中心频率 Hz
        c = ssf_paras['c']                                                  # 光速 m/s
        ATT = ssf_paras['ATT']
        chirp_num = ssf_paras['chirp_num']                                  # chirp 数目 3秒 1933+1933+1934 (可能会引起后面作图错误)
        window = ssf_paras['window']                                        # 窗设置 例如此处设为 20 lambda
        win_wide = ssf_paras['win_wide']
        beg_p = ssf_paras['beg_p']                                          # 数据起始点设置 从第二个 chirp开始 (由于第一个chirp不对所有的RSL数据都比RX位置数据多了1, 但此处也要注意) 2对应了GPS坐标1
        end_p = ssf_paras['end_p']                                          # 数据终止点设置 32对应了GPS坐标31
        beg_t_mark = ssf_paras['beg_t_mark']                                # 起始点时间序号 例如此数据共50s 因此 此时值为 0
        cable1 = ssf_paras['cable1']                                        # 线损 3dB
        cable2 = ssf_paras['cable2']                                        # 线损 3dB
        TX_power = ssf_paras['TX_power']                                    # 天线发射功率 16 dBm
        G_TX = ssf_paras['TX_Gain']                                         # 发射天线增益 2 dBi
        G_RX = ssf_paras['RX_Gain']                                         # 接收天线增益 2 dBi
        h_1 = ssf_paras['TX_heigh'] / 1000                                  # 发射天线有效高度 km
        h_2 = ssf_paras['RX_heigh'] / 1000                                  # 接收天线有效高度 km
        SM_time = ssf_paras['SM_time']
        SM_distance = ssf_paras['SM_distance']
        NB_signal = ssf_data['NB_signal']
        PL_no_SM = ssf_data['PL_no_SM']
        Small_scale_fading = ssf_data['Small_scale_fading']
        
        '''
        取用数据设置
        '''
        beg_point = kwargs['small_scale_beg_point']
        end_point = kwargs['small_scale_end_point']
        T = SM_time[beg_point-1 : end_point]
        Dis = SM_distance[beg_point-1 : end_point]
        RSL_all = NB_signal[beg_point-1 : end_point]
        RSL_n_ssf = PL_no_SM[beg_point-1 : end_point]
        SSF = Small_scale_fading[beg_point-1 : end_point]
        ssf1 = 10 ** (SSF / 10)
        beg_ssf_point = kwargs['small_scale_beg_ssf_point']
        end_ssf_point = kwargs['small_scale_end_ssf_point']
        ssf = ssf1[beg_ssf_point-1 : end_ssf_point]
        data_length = np.shape(ssf)[0]
        
        '''
        运行程序开始
        '''
        '''
        LCR & AFD
        '''
        LCR_total, AFD_total, Threshold = Meas_LCR_AFD(ssf)
        com_time = data_length / win_wide
        LCR_per_second = LCR_total / com_time
        AFD = AFD_total / data_length
        Amp_NB = ssf ** 0.5
        Amp_all_NB = ssf1 ** 0.5
        Threshold = 10 * np.log10(Threshold)
        
        '''
        图形生成程序
        '''
        T = T - np.min(T) + 1
        
        '''
        绘制保存fig1
        '''
        fig = plt.figure(tight_layout = True)
        
        ax = fig.add_subplot(211)
        ax.plot(T, RSL_all, 'b')
        ax.plot(T, RSL_n_ssf, 'g')
        ax.grid(True)
        
        ax = fig.add_subplot(212)
        ax.plot(T, SSF, 'b')
        ax.grid(True)
        
        plt.savefig('./results/power_domain/small_scale_fading_mainfunction_fig1.png')
        plt.clf()
        # 保存此图变量
        np.savez('./plot_params/small_scale_fading_mainfunction_fig1.npz', T=T, RSL_all=RSL_all, RSL_n_ssf=RSL_n_ssf, SSF=SSF)
        
        '''
        绘制保存fig2
        '''
        fig = plt.figure(tight_layout = True)
    
        ax = fig.add_subplot(211)
        ax.plot(Dis, RSL_all, 'b')
        ax.plot(Dis, RSL_n_ssf, 'g')
        ax.grid(True)
    
        ax = fig.add_subplot(212)
        ax.plot(Dis, SSF, 'b')
        ax.grid(True)
    
        plt.savefig('./results/power_domain/small_scale_fading_mainfunction_fig2.png')
        plt.clf()
        # 保存此图变量
        np.savez('./plot_params/small_scale_fading_mainfunction_fig2.npz', Dis=Dis, RSL_all=RSL_all, RSL_n_ssf=RSL_n_ssf, SSF=SSF)
        
        '''
        绘制保存fig3
        '''
        fig = plt.figure(tight_layout = True)
        
        ax = fig.add_subplot(111)
        ax.plot(Dis, RSL_all, 'b', linewidth = 2.0)
        ax.set_xlabel('Distance in m', fontproperties = 'Times New Roman', fontsize = 8)
        ax.set_ylabel('Received signal level in dBm', fontproperties = 'Times New Roman', fontsize = 8)
        ax.grid(True)
        
        plt.savefig('./results/power_domain/small_scale_fading_mainfunction_fig3.png')
        plt.clf()
        # 保存此图变量
        np.savez('./plot_params/small_scale_fading_mainfunction_fig3.npz', Dis=Dis, RSL_all=RSL_all)
        
        '''
        绘制保存fig4
        '''
        fig = plt.figure(tight_layout = True)
        ax = fig.add_subplot(111)
    
        ax.plot(T, RSL_all, 'b-', linewidth = 1.5, label = 'Measurement data')
        ax.plot(T, RSL_n_ssf, 'r-', linewidth = 1.5, label = 'Estimation data')
    
        ax.set_xlim(np.min(T), np.max(T))
        ax.set_ylim(min(np.min(RSL_all), np.min(RSL_n_ssf)), max(np.max(RSL_all), np.max(RSL_n_ssf)))
        ax.set_xlabel('Time in s', fontproperties = 'Times New Roman', fontsize = 10)
        ax.set_ylabel('Received signal level (no small scale fading) in dBm', fontproperties = 'Times New Roman', fontsize = 10)
        ax.grid(True)
        plt.legend(bbox_to_anchor=(1.0, 1), loc=1, borderaxespad=0.5)
    
        plt.savefig('./results/power_domain/small_scale_fading_mainfunction_fig4.png')
        plt.clf()
        # 保存此图变量
        np.savez('./plot_params/small_scale_fading_mainfunction_fig4.npz', T=T, RSL_all=RSL_all, RSL_n_ssf=RSL_n_ssf)
        
        '''
        绘制保存fig5
        '''
        fig = plt.figure(tight_layout = True)
        ax = fig.add_subplot(111)
    
        ax.plot(T, SSF, 'b', linewidth = 1.5)
    
        ax.set_xlim(np.min(T), np.max(T))
        ax.set_ylim(np.min(SSF), np.max(SSF))
        ax.set_xlabel('Time in s', fontproperties = 'Times New Roman', fontsize = 10)
        ax.set_ylabel('Small scale fading in dB', fontproperties = 'Times New Roman', fontsize = 10)
        ax.grid(True)
        
        plt.savefig('./results/power_domain/small_scale_fading_mainfunction_fig5.png')
        plt.clf()
        # 保存此图变量
        np.savez('./plot_params/small_scale_fading_mainfunction_fig5.npz', T=T, SSF=SSF)
        
        '''
        绘制保存fig6
        '''
        fig = plt.figure(tight_layout = True)
        ax = fig.add_subplot(111)
        
        lowess_LCR_per_second = lowess(LCR_per_second, Threshold, frac=0.03, it = 0)
        ax.plot(lowess_LCR_per_second[:, 0], lowess_LCR_per_second[:, 1], 'b', linewidth = 1.5)
    
        ax.set_xlim(-0.5, 0.5)
        ax.set_ylim(np.min(LCR_per_second), np.max(LCR_per_second))
        ax.set_xlabel('Threshold in dB', fontproperties = 'Times New Roman', fontsize = 10)
        ax.set_ylabel('LCR (times per second)', fontproperties = 'Times New Roman', fontsize = 10)
        ax.grid(True)
    
        plt.savefig('./results/power_domain/small_scale_fading_mainfunction_fig6.png')
        plt.clf()
        # 保存此图变量
        np.savez('./plot_params/small_scale_fading_mainfunction_fig6.npz', lowess_LCR_per_second=lowess_LCR_per_second, LCR_per_second=LCR_per_second)
        
        '''
        绘制保存fig7
        '''
        fig = plt.figure(tight_layout = True)
        ax = fig.add_subplot(111)
    
        lowess_AFD = lowess(AFD, Threshold, frac=0.03, it = 0)
        ax.plot(lowess_AFD[:, 0], lowess_AFD[:, 1], 'b', linewidth = 1.5)
    
        ax.set_xlim(-0.5, 0.5)
        ax.set_ylim(np.min(AFD), np.max(AFD))
        ax.set_xlabel('Threshold in dB', fontproperties = 'Times New Roman', fontsize = 10)
        ax.set_ylabel('ADF (seconds)', fontproperties = 'Times New Roman', fontsize = 10)
        ax.grid(True)
    
        plt.savefig('./results/power_domain/small_scale_fading_mainfunction_fig7.png')
        plt.clf()
        # 保存此图变量
        np.savez('./plot_params/small_scale_fading_mainfunction_fig7.npz', lowess_AFD=lowess_AFD, AFD=AFD)
        
        '''
        绘制保存fig8
        '''
        fig = plt.figure(tight_layout = True)
        ax = fig.add_subplot(111)
        
        ax.plot(SSF, 'b', linewidth = 1.5)
        
        plt.savefig('./results/power_domain/small_scale_fading_mainfunction_fig8.png')
        plt.clf()
        # 保存此图变量
        np.savez('./plot_params/small_scale_fading_mainfunction_fig8.npz', SSF=SSF)
        
        plt.close('all')
        
        
        if debug_mode:
            print('NB_signal')
            print(NB_signal.shape)
            print('PL_no_SM')
            print(PL_no_SM.shape)
            print('Small_scale_fading')
            print(Small_scale_fading.shape)
            print('ssf')
            print(ssf.shape)
            print(ssf[0:6])
            print(ssf[-6:])
            print('SSF')
            print(SSF.shape)
            print(SSF[0:6])
            print('LCR_per_second')
            print(LCR_per_second.shape)
            print(LCR_per_second[0:6])
            print(LCR_per_second[300:306])
            print(LCR_per_second[-6:])
            print('AFD')
            print(AFD.shape)
            print(AFD[0:6])
            print(AFD[300:306])
            print(AFD[-6:])
            print('Threshold')
            print(Threshold.shape)
            print(Threshold[0:6])
            print(Threshold[300:306])
            print(Threshold[-6:])            
            
if __name__ == '__main__':
    begin_time = timeit.default_timer()
    
    small_scale_fading()
    
    end_time = timeit.default_timer()
    print('Running time')
    print(str(end_time - begin_time))
