# coding=utf-8
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import timeit
import os
import sys

from Main_function_and_doppler.txt_read import txt_read
from Main_function_and_doppler.xls_read import tx_xls_read, rx_xls_read
from Main_function_and_doppler.Att_mark import Att_mark
from Main_function_and_doppler.GPS_2_distance import GPS_2_distance
from Main_function_and_doppler.signal_window import signal_window
from Main_function_and_doppler.CIR_window import CIR_window
from Main_function_and_doppler.distance_match import distance_match
from Main_function_and_doppler.time_match import time_match
from Main_function_and_doppler.speed_match import speed_match
from Main_function_and_doppler.MakeChirp import MakeChirp
from Main_function_and_doppler.small_scale_match import small_scale_match

class main_doppler():
    def __init__(self, **kwargs):
        '''
        设置Debug模式
        '''
        debug_mode = False
        
        '''
        读取txt, xls的信息
        '''
        txt_info = txt_read(kwargs['txt_folder'])
        
        '''
        设置t_start和t_stop
        '''
        t_start = kwargs['t_start']                                    # 读取excel的开始时间，第几行，包括这一行
        t_stop = t_start + txt_info.txt_num - 1                        # 读取excel的结束时间，第几行，包括这一行
        
        '''
        从UI选择的文件夹里选择xls文件
        '''
        rx_file, tx_file = self.xls_folder_process(kwargs['xls_folder'])
        '''
        --------------------------------------------------------------------------------------
        '''
        tx_xls = tx_xls_read(tx_file, t_start, t_stop)
        rx_xls = rx_xls_read(rx_file, t_start, t_stop)
        
        signal_CIR = txt_info.signal_CIR                               # signal_CIR为一个(txt文件数目)大小的列表
        GPS_rx = rx_xls.GPS_rx
        GPS_tx = tx_xls.GPS_tx
        v_tx = tx_xls.v_tx
        v_rx = rx_xls.v_rx
        rel_speed = np.maximum(v_tx, v_rx)
        
        '''
        -------------------------------------------------------------------------------------
        对数据进行裁剪
        -------------------------------------------------------------------------------------
        '''
        d = GPS_2_distance(GPS_rx, GPS_tx)
        Dis = d * 1000
        t_los_min = np.min(Dis, axis=0) / 3e8
        num_sample = np.ceil(t_los_min / 10e-9)
        num_cell_row = len(signal_CIR)
        
        for n in range(0, num_cell_row):
            signal_CIR[n][:, 0] = signal_CIR[n][:, 1] - np.random.rand(1, 1) / 1e4
        
        index_max = []
        value_max = []
        for n in range(0, num_cell_row):
            cache = np.abs(signal_CIR[n])
            value_max.append(np.max(np.max(cache)))
            index_max.append((np.where(cache == value_max[n]))[-1][0] + 1)
        value_max = np.array(value_max).astype('int64')
        index_max = np.array(index_max).astype('int64')
        
        value = np.max(value_max, axis=0)
        index = np.where(value_max == value)[0][0] + 1
        index_cut = index_max[index - 1]
        cutting_point = int(index_cut - num_sample - 3)
        
        for i in range(0, num_cell_row):
            num_row = np.shape(signal_CIR[i])[0]
            for j in range(0, num_row):
                signal_CIR[i][j, :] = np.concatenate((signal_CIR[i][j, (cutting_point + 1 - 1) : int(np.shape(
                    signal_CIR[i])[-1])], signal_CIR[i][j, 0:cutting_point]))
        
        '''
        -------------------------------------------------------------------------------------
        '''
        
        '''
        测试参数设置
        '''
        beg_p = 1                                                      # 数据起始点设置，从第二个chirp开始(由于第一个chirp不对所有的RSL数据都比RX位置数据多了1, 但此处也要注意)2对应了GPS坐标1
        end_p = txt_info.txt_num                                       # 数据终止点设置，32对应了GPS坐标31
        window = kwargs['window']                                      # 窗设置，例如此处设为 20 lambda
        beg_t_mark = 0                                                 # 起始点时间序号，例如此数据共50s，因此，此时值为 0
        t_res = 10                                                     # unit:ns,esolution
        
        '''
        天线参数设置
        '''
        TX_power = kwargs['TX_power']                                  # 天线发射功率 16 dBm
        TX_Gain = kwargs['TX_Gain']                                    # 发射天线增益 2 dBi
        RX_Gain = kwargs['RX_Gain']                                    # 接收天线增益 2 dBi
        TX_heigh = kwargs['TX_heigh']                                  # 发射天线有效高度 m
        RX_heigh = kwargs['RX_heigh']                                  # 接收天线有效高度 m
        
        '''
        瞬时多普勒频移需要的参数
        '''
        T_doppler = 2                                                  # 第 20 秒的多普勒频移
        num_file = 2                                                   # 选择多少个窗作多普勒频移
        
        '''
        设备参数设置
        '''
        fc = kwargs['fc']                                              # 载波中心频率 Hz
        c = 3e8                                                        # 光速 m/s
        ATT_mark = kwargs['ATT_mark']                                  # 衰减系数ATT为8
        ATT = Att_mark(ATT_mark)
        chirp_num = kwargs['chirp_num']                                # chirp数目3秒1933+1933+1934(可能会引起后面作图错误)
        cable1 = 0                                                     # 线损3dB
        cable2 = kwargs['cable'] - cable1                              # 线损3dB
        
        '''
        测试数据读取
        '''
        ave_speed =np.mean(rel_speed)                                  # 平均相对速度 m/s
        max_speed = np.max(rel_speed)                                  # 最大相对速度 m/s
        
        '''
        数据生成程序
        '''
        data = []
        cir = []
        data_pdp = [0] * (end_p - beg_p + 1)
        CIR_1 = [0] * (end_p - beg_p + 1)
        for n in range(beg_p - 1, end_p):
            data_pdp[n] = ATT * np.power(np.absolute(signal_CIR[n]), 2)
            data_pdp[n][:, 0] = data_pdp[n][:, 1]                                                       # 去掉起始点的突起
            CIR_1[n] = signal_CIR[n][:]                                                                 # 原始 CIR 信号 cell
            CIR_1[n][:, 0] = CIR_1[n][:, 1] - np.random.rand(1, 1) / 1e4                                # 去掉起始点的突起 rand是为了防止出现多普勒频移处找点重合的问题
        
        del signal_CIR[:]                                                                               # 清除缓存数据
        del txt_info.signal_CIR[:]
        
        T = rx_xls.T                                                                                    # 注意：若第一个文件是有效的那要把1改为其它对应时间
        d = GPS_2_distance(GPS_rx, GPS_tx)                                                              # d units: km
        Dis = d * 1000                                                                                  # Dis units: m
        max_v = max_speed.copy()                                                                        # 最大相对速度用于取窗
        win_wide = np.floor(window * (chirp_num * (c / fc)) / max_v)                                    # 窗宽 units: chirp
        after_window = signal_window(win_wide, data_pdp)
        del data_pdp[:]
        after_window_cir = CIR_window(win_wide, CIR_1)
        distance = distance_match(after_window, Dis)
        time = time_match(after_window, T)
        V_rel = speed_match(after_window, rel_speed)
        num_a = np.shape(distance)[0]
        pdp_window = after_window[0]
        D_window = distance[0]
        TIME = time[0]
        V_Rel = V_rel[0]
        for i in range(0, num_a - 1):
            pdp_window = np.row_stack((pdp_window, after_window[i + 1]))
            D_window = np.concatenate((D_window, distance[i + 1]), axis = 0)
            TIME = np.concatenate((TIME, time[i + 1]), axis = 0)
            V_Rel = np.concatenate((V_Rel, V_rel[i + 1]), axis = 0)
        CIR_window_doppler = after_window_cir[0 : np.shape(TIME)[0]]
        del after_window_cir[:]
        del CIR_1[:]
        del distance[:]
        del time[:]
        del V_rel[:]
        
        '''
        获取振幅分布数据
        '''
        AIC_data = CIR_window_doppler[:]
        NA = len(AIC_data)                                                                              # 按照分段获取数组范围( 20*lambda )
        Chirp_t = MakeChirp(SampFreqDec = 1 / 8.125e-9, ChirpBandw = 100e6, NchirpDec = np.shape(AIC_data[0])[-1])           # 产生模拟标准chirp信号
        Chirp_f = np.fft.fftshift(np.fft.fft(np.conj(np.flipud(Chirp_t)), axis = 0))                    # 为除去卷积chirp信号做准备
        AIC_com = []
        AIC_DATA = []

        for pot in range(0, NA):                                                                        # 循环获取每个分段内的AIC标准数据
            AIC_data_t = []
            aic_data = AIC_data[pot].T
            data_f = np.fft.fft(aic_data, axis = 0)
            nb = np.shape(data_f)[1]
            for n in range(0, nb):                                                                      # 循环堆积每段内的标准数据
                Data_f = np.concatenate((np.zeros(279), data_f[279:2281, n], np.zeros(2560 - 2281)), axis = 0)
                AIC_data_f = Data_f / Chirp_f
                AIC_data_t = np.concatenate((AIC_data_t, np.fft.ifft(AIC_data_f, axis = 0)))
            AIC_com.append(AIC_data_t)
            AIC_DATA.append(np.abs(AIC_data_t))
        del AIC_data_t
        del AIC_com[:]
        del AIC_data[:]
        del Chirp_t
        
        '''
        等效窄带信号获取处理
        '''
        distance_sm = small_scale_match(CIR_window_doppler, D_window)                                   # 与小尺度匹配的距离信息 注意因为差分的缘故比正常少一个cell
        time_sm = small_scale_match(CIR_window_doppler, TIME)                                           # 与小尺度匹配的时间信息 注意因为差分的缘故比正常少一个cell
        num_sm1 = np.shape(CIR_window_doppler)[0]
        SM_time = []
        SM_distance = []
        PL_no_sm = []
        L = 0
        C = 0
        for num in range(0, num_sm1 - 1):                                                               # 注意因为差分的缘故比正常少一个cell 因此此处num_sm1 - 1
            L = np.shape(CIR_window_doppler[num])[0]
            C = np.shape(CIR_window_doppler[num])[1]
            ave_sm = ATT * np.power(np.abs(CIR_window_doppler[num]), 2)
            Ave_sm = np.sum(np.sum(ave_sm, axis = 1) / C, axis = 0) / L
            PL_no_sm = np.concatenate((PL_no_sm, np.linspace(Ave_sm, Ave_sm, L)))
            SM_time = np.concatenate((SM_time, time_sm[num]))
            SM_distance = np.concatenate((SM_distance, distance_sm[num]))
            
        del distance_sm[:]
        del time_sm[:]
        
        Equ_Narr_band = CIR_window_doppler[0]
        for num in range(1, num_sm1 - 1):
            Equ_Narr_band = np.concatenate((Equ_Narr_band, CIR_window_doppler[num]), axis = 0)
            
        Narrow_band_signal = ATT * np.abs(np.power(Equ_Narr_band[0:np.shape(SM_time)[0], :], 2))
        NB_signal = 10 * np.log10(np.sum(Narrow_band_signal, axis = 1) / C)
        PL_no_SM = 10 * np.log10(PL_no_sm)
        Small_scale_fading = NB_signal - PL_no_SM
        TIME = TIME + beg_t_mark                                                                        # 平移时间
        Equ_Narr_band = []
        Narrow_band_signal = []
        
        '''
        多普勒频移处理
        '''
        num_aa = len(CIR_window_doppler)
        fre_resolution = np.floor(chirp_num) / win_wide
        Hz_x = np.flipud(np.arange(-np.floor(chirp_num / 2), np.floor(chirp_num / 2) + fre_resolution / 10e4, fre_resolution))  # 以窗为单位的多普勒频移再翻转
        fre_domain = []
        for_dop = []
        fre_nor_domain = []
        idx = []
        p_Hz = []
        p_De = []
        for n in range(0, num_aa):
            # 未归一化数据 注意这里fftshift至关重要
            fre_domain.append(10 * np.log10(ATT * np.power(np.abs(np.fft.fftshift(np.fft.fft(CIR_window_doppler[n], axis=0), axes=(0, ))), 2)))
            for_dop.append(np.power(np.abs(np.fft.fftshift(np.fft.fft(CIR_window_doppler[n], axis=0), axes=(0, ))), 2))
            fre_nor_domain.append(fre_domain[n] - np.max(np.max(fre_domain[n])))                        # 归一化因为是dB形式故而相减
            idx = np.where(fre_nor_domain[n] == np.max(np.max(fre_nor_domain[n])))
            p_Hz.append(idx[0][0])
            p_De.append(idx[1][0])
        p_Hz = np.array(p_Hz)
        p_De = np.array(p_De)
        del fre_domain[:]
        
        Max_doppler = []
        for n in range(0, num_aa):
            Max_doppler.append(Hz_x[p_Hz[n]])                                                           # 最大多普勒频移记录 units: Hz
        Max_doppler = np.array(Max_doppler)
        
        '''
        瞬时多普勒频移制图需要
        '''
        idx = np.where(TIME == T_doppler + T[0])
        d_begp = np.max(idx[0])                                                                         # 确认起始点
        d_endp = d_begp + num_file                                                                      # 确认终止点 以 0.5 s 为单位的多普勒频移 取一半的文件 
        CIR_D = CIR_window_doppler[d_begp : d_endp + 1]
        num_Da = len(CIR_D)
        
        del CIR_window_doppler[:]
        
        CIR_doppler = CIR_D[0]
        for n in range(1, num_Da):
            CIR_doppler = np.concatenate((CIR_doppler, CIR_D[n]))
        
        del CIR_D[:]
            
        # 具体秒数多普勒频移
        fre_in_domain = 10 * np.log10(ATT * np.power(np.abs(np.fft.fftshift(np.fft.fft(CIR_doppler, axis=0), axes=(0, ))), 2))
        Fre_innor_domain = fre_in_domain - np.max(np.max(fre_in_domain))                                # 归一化操作
        Fre_resolution = np.floor(chirp_num) / (win_wide * np.arange(d_begp, d_endp + 0.1).shape[0])
        # 瞬时多普勒频移再翻转
        Hz_in_x = np.flipud(np.arange(-np.floor(chirp_num / 2), np.floor(chirp_num / 2) + Fre_resolution / 10e4, Fre_resolution))
        RSL = 10 * np.log10(np.sum(pdp_window, axis = 1) / np.shape(pdp_window)[-1])                    # RSL units: dBm
        channel_gain = RSL + cable1 + cable2 - TX_power - TX_Gain - RX_Gain
        
        AAA = len(fre_nor_domain)
        num_AA = []
        num_BB = []
        for nn in range(0, AAA):
            idx = np.where(fre_nor_domain[nn] == np.max(np.max(fre_nor_domain[nn])))
            num_AA.append(idx[0][0])
            num_BB.append(idx[1][0])
        num_AA = np.array(num_AA)
        num_BB = np.array(num_BB)
        
        LOS_doppler = Hz_x[num_AA]
        LOS_delay = (num_BB + 1) * t_res
        
        '''
        图形生成程序
        '''
        TIME = TIME - np.min(TIME) + 1
        
        '''
        绘制保存fig1
        '''
        #fig = plt.figure(figsize=(8, 6), dpi=100, tight_layout=True)
        # 自动控制排版
        fig = plt.figure(1, tight_layout = True, clear=True)
        
        ax = fig.add_subplot(211)
        X, Y = np.meshgrid(TIME, np.arange(t_res, t_res * 2560 + t_res / 10e4, t_res))
        Z = 10 * np.log10(pdp_window.T)
        
        ax.contourf(X, Y, Z, cmap = cm.jet)
        ax.set_xlim(np.min(TIME), np.max(TIME))
        ax.set_ylim(0, t_res * 400)
        #ax.set_xticks(np.linspace(np.min(TIME), np.max(TIME), 11, endpoint = True))
        #ax.set_yticks(np.linspace(0, t_res * 400, 5, endpoint = True))
        ax.set_xlabel('Time in s', fontproperties = 'Times New Roman', fontsize = 10)
        ax.set_ylabel('Delay in ns', fontproperties = 'Times New Roman', fontsize = 10)
        
        ax = fig.add_subplot(212)
        ax.plot(TIME, channel_gain, 'b',linewidth = 2.0)
        ax.set_xlim(np.min(TIME), np.max(TIME))
        ax.set_ylim(np.min(channel_gain), np.max(channel_gain))
        #ax.set_xticks(np.linspace(np.min(TIME), np.max(TIME), 11, endpoint = True))
        #ax.set_yticks(np.linspace(np.min(channel_gain), np.max(channel_gain), 5, endpoint = True))
        ax.set_xlabel('Time in s', fontproperties = 'Times New Roman', fontsize = 10)
        ax.set_ylabel('Channel gain in dB', fontproperties = 'Times New Roman', fontsize = 10)
        # 显示网格
        ax.grid(True)
        
        plt.savefig('./results/Main_function_and_doppler/Main_function_and_doppler_fig1.png')
        plt.clf()
        plt.cla()
        plt.close(fig)
        # 保存此图变量
        np.savez('./plot_params/Main_function_and_doppler_fig1.npz', TIME=TIME, t_res=t_res, pdp_window=pdp_window, channel_gain=channel_gain)
        
        '''
        绘制保存fig11
        绘制3d图像, rstride=1, cstride=1相当耗时
        '''
        fig = plt.figure(11, tight_layout = True, clear=True)
        ax = fig.add_subplot(111, projection = '3d')
        ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.jet, linewidth=0, antialiased=False)
        ax.view_init(None, 30)
        ax.set_xlabel('Time in s', fontproperties = 'Times New Roman', fontsize = 10)
        ax.set_zlabel('Delay in ns', fontproperties = 'Times New Roman', fontsize = 10)
        
        plt.savefig('./results/Main_function_and_doppler/Main_function_and_doppler_fig11.png')
        plt.clf()
        plt.cla()
        plt.close(fig)
        del X, Y, Z
        # 保存此图变量
        np.savez('./plot_params/Main_function_and_doppler_fig11.npz', TIME=TIME, t_res=t_res, pdp_window=pdp_window)
        
        '''
        绘制保存fig2
        '''
        sec = 5
        num_win = 2
        
        X = np.arange(t_res, t_res * 2560 + t_res / 10e4, t_res)
        Y = 10 * np.log10(after_window[sec - 1][num_win - 1, :])
        
        fig = plt.figure(2, tight_layout = True, clear=True)
        ax = fig.add_subplot(111)
        ax.plot(X, Y, 'b', linewidth = 2)
        ax.set_xlim(0, t_res * 2560)
        ax.set_ylim(np.min(Y), np.max(Y))
        ax.set_xlabel('Time in ns', fontproperties = 'Times New Roman', fontsize = 10)
        ax.set_ylabel('Average PDP in dB', fontproperties = 'Times New Roman', fontsize = 10)
        ax.grid(True)
        
        plt.savefig('./results/Main_function_and_doppler/Main_function_and_doppler_fig2')
        plt.clf()
        plt.cla()
        plt.close(fig)
        # 保存此图变量
        np.savez('./plot_params/Main_function_and_doppler_fig2.npz', X=X, Y=Y, t_res=t_res)
        del X, Y
        
        '''
        绘制保存fig3
        '''
        n = 35
        
        X = np.arange(t_res / 1000, t_res * 2560 / 1000 + t_res / 1000 / 10e4, t_res / 1000)
        Y = Hz_x.copy()
        X, Y = np.meshgrid(X, Y)
        Z = fre_nor_domain[n - 1]
        del fre_nor_domain[:]
        
        fig = plt.figure(3, tight_layout = True, clear=True)
        ax = fig.add_subplot(111)
        ax.contourf(X, Y, Z, cmap = cm.jet)
        ax.set_xlim(0, 5)
        ax.set_ylim(-966, 966)
        ax.set_xlabel('Time in us', fontproperties = 'Times New Roman', fontsize = 10)
        ax.set_ylabel('Doppler Frequency in Hz', fontproperties = 'Times New Roman', fontsize = 10)
        
        plt.savefig('./results/Main_function_and_doppler/Main_function_and_doppler_fig3')
        plt.clf()
        plt.cla()
        plt.close(fig)
        # 保存此图变量
        np.savez('./plot_params/Main_function_and_doppler_fig3.npz', X=X, Y=Y, Z=Z)
        del X, Y, Z
        
        '''
        绘制保存fig4
        '''
        X = np.arange(t_res, t_res * 2560 + t_res / 10e4, t_res)
        Y = Hz_in_x.copy()
        X, Y = np.meshgrid(X, Y)
        Z = Fre_innor_domain[0 : np.shape(Hz_in_x)[0], :]
    
        fig = plt.figure(4, tight_layout = True, clear=True)
        ax = fig.add_subplot(111)
        ax.contourf(X, Y, Z, cmap = cm.jet)
        ax.set_xlim(0, 2000)
        ax.set_ylim(-966, 966)
        ax.set_xlabel('Delay in us', fontproperties = 'Times New Roman', fontsize = 10)
        ax.set_ylabel('Doppler Frequency in Hz', fontproperties = 'Times New Roman', fontsize = 10)
    
        plt.savefig('./results/Main_function_and_doppler/Main_function_and_doppler_fig4')
        plt.clf()
        plt.cla()
        plt.close(fig)
        # 保存此图变量
        np.savez('./plot_params/Main_function_and_doppler_fig4.npz', X=X, Y=Y, Z=Z)
        del X, Y, Z
        
        '''
        绘制保存fig5
        '''
        fig = plt.figure(5, tight_layout = True, clear=True)
        ax = fig.add_subplot(111)
        ax.plot(SM_time, NB_signal, 'b-')
        ax.plot(SM_time, PL_no_SM, 'r-')
        ax.set_xlabel('time in seconds', fontproperties = 'Times New Roman', fontsize = 10)
        ax.set_ylabel('RSL in dBm', fontproperties = 'Times New Roman', fontsize = 10)
        ax.grid(True)
    
        plt.savefig('./results/Main_function_and_doppler/Main_function_and_doppler_fig5')
        plt.clf()
        plt.cla()
        plt.close(fig)
        # 保存此图变量
        np.savez('./plot_params/Main_function_and_doppler_fig5.npz', SM_time=SM_time, NB_signal=NB_signal, PL_no_SM=PL_no_SM)
        
        '''
        绘制保存fig6
        '''
        X = SM_time.copy()
        Y = Small_scale_fading.copy()
    
        fig = plt.figure(6, tight_layout = True, clear=True)
        ax = fig.add_subplot(111)
        ax.plot(X, Y, 'b')
        ax.set_xlim(np.min(X), np.max(X))
        ax.set_ylim(np.min(Y), np.max(Y))
        ax.set_xlabel('time in seconds', fontproperties = 'Times New Roman', fontsize = 10)
        ax.set_ylabel('Small_scale_fading in dB', fontproperties = 'Times New Roman', fontsize = 10)
        ax.grid(True)
    
        plt.savefig('./results/Main_function_and_doppler/Main_function_and_doppler_fig6')
        plt.clf()
        plt.cla()
        plt.close(fig)
        # 保存此图变量
        np.savez('./plot_params/Main_function_and_doppler_fig6.npz', X=X, Y=Y)
        del X, Y
        
        '''
        绘制保存fig8
        '''
        X = TIME.copy()
        Y = channel_gain.copy()
        
        fig = plt.figure(8, tight_layout = True, clear=True)
        ax = fig.add_subplot(111)
        ax.plot(X, Y, 'b')
        ax.set_xlim(np.min(X), np.max(X))
        ax.set_ylim(np.min(Y), np.max(Y))
        ax.set_xlabel('Time in s', fontproperties = 'Times New Roman', fontsize = 10)
        ax.set_ylabel('Channel gain in dB', fontproperties = 'Times New Roman', fontsize = 10)
        ax.grid(True)
    
        plt.savefig('./results/Main_function_and_doppler/Main_function_and_doppler_fig8')
        plt.clf()
        plt.cla()
        plt.close(fig)
        # 保存此图变量
        np.savez('./plot_params/Main_function_and_doppler_fig8.npz', X=X, Y=Y)
        del X, Y
        
        plt.close('all')
        
        '''
        保存变量
        '''
        np.savez('./params/delay_paras.npz', fc = fc, c = c, ATT = ATT, chirp_num = chirp_num, window = window, 
                 beg_p = beg_p, end_p = end_p, beg_t_mark = beg_t_mark, cable1 = cable1, cable2 = cable2, 
                 TX_power = TX_power, TX_Gain = TX_Gain, RX_Gain = RX_Gain, TX_heigh = TX_heigh, RX_heigh = RX_heigh,
                 TIME = TIME, D_window = D_window, v_rx = v_rx, v_tx = v_tx)
        #np.savez('./params/delay_data.npz', after_window = np.array(after_window).reshape((len(after_window), after_window[0].shape[0], after_window[0].shape[1])))
        np.savez('./params/delay_data.npz', after_window = after_window)
        np.savez('./params/ssf_paras.npz', fc = fc, c = c, ATT = ATT, chirp_num = chirp_num, window = window, 
                 beg_p = beg_p, end_p = end_p, beg_t_mark = beg_t_mark, cable1 = cable1, cable2 = cable2, 
                 TX_power = TX_power, TX_Gain = TX_Gain, RX_Gain = RX_Gain, TX_heigh = TX_heigh, RX_heigh = RX_heigh,
                 TIME = TIME, D_window = D_window, v_rx = v_rx, v_tx = v_tx, win_wide = win_wide, SM_time = SM_time,
                 SM_distance = SM_distance)
        np.savez('./params/ssf_data.npz', NB_signal = NB_signal, PL_no_SM = PL_no_SM, Small_scale_fading = Small_scale_fading)
        #np.savez('./params/Amp_DATA.npz', AIC_DATA = np.array(AIC_DATA).reshape(len(AIC_DATA), 1, AIC_DATA[0].shape[-1]))
        np.savez('./params/Amp_DATA.npz', AIC_DATA = AIC_DATA)
        np.savez('./params/PL_paras.npz', fc = fc, c = c, ATT = ATT, chirp_num = chirp_num, window = window, 
                 beg_p = beg_p, end_p = end_p, beg_t_mark = beg_t_mark, cable1 = cable1, cable2 = cable2, 
                 TX_power = TX_power, TX_Gain = TX_Gain, RX_Gain = RX_Gain, TX_heigh = TX_heigh, RX_heigh = RX_heigh,
                 TIME = TIME, D_window = D_window, v_rx = v_rx, v_tx = v_tx)
        np.savez('./params/PL_data.npz', RSL = RSL)
        np.savez('./params/PDP_paras.npz', fc = fc, c = c, ATT = ATT, chirp_num = chirp_num, window = window, 
                 beg_p = beg_p, end_p = end_p, beg_t_mark = beg_t_mark, cable1 = cable1, cable2 = cable2, 
                 TX_power = TX_power, TX_Gain = TX_Gain, RX_Gain = RX_Gain, TX_heigh = TX_heigh, RX_heigh = RX_heigh,
                 TIME = TIME, D_window = D_window, v_rx = v_rx, v_tx = v_tx)
        np.savez('./params/PDP_data.npz', pdp_window = pdp_window)
        np.savez('./params/fre_paras.npz', fc = fc, c = c, ATT = ATT, chirp_num = chirp_num, window = window, 
                 beg_p = beg_p, end_p = end_p, beg_t_mark = beg_t_mark, cable1 = cable1, cable2 = cable2, 
                 TX_power = TX_power, TX_Gain = TX_Gain, RX_Gain = RX_Gain, TX_heigh = TX_heigh, RX_heigh = RX_heigh,
                 TIME = TIME, D_window = D_window, v_rx = v_rx, v_tx = v_tx)
        np.savez('./params/fre_data.npz', LOS_doppler = LOS_doppler, LOS_delay = LOS_delay)
        np.savez('./params/channelgain_paras.npz', fc = fc, c = c, ATT = ATT, chirp_num = chirp_num, window = window, 
                 beg_p = beg_p, end_p = end_p, beg_t_mark = beg_t_mark, cable1 = cable1, cable2 = cable2, 
                 TX_power = TX_power, TX_Gain = TX_Gain, RX_Gain = RX_Gain, TX_heigh = TX_heigh, RX_heigh = RX_heigh,
                 TIME = TIME, D_window = D_window, v_rx = v_rx, v_tx = v_tx)
        np.savez('./params/channelgain_data.npz', channel_gain = channel_gain)
        np.savez('./params/dop_paras.npz', fc = fc, c = c, ATT = ATT, chirp_num = chirp_num, window = window, 
                 beg_p = beg_p, end_p = end_p, beg_t_mark = beg_t_mark, cable1 = cable1, cable2 = cable2, 
                 TX_power = TX_power, TX_Gain = TX_Gain, RX_Gain = RX_Gain, TX_heigh = TX_heigh, RX_heigh = RX_heigh,
                 TIME = TIME, D_window = D_window, v_rx = v_rx, v_tx = v_tx, Hz_x = Hz_x)
        #np.savez('./params/dop_data.npz', for_dop = np.array(for_dop).reshape((len(for_dop), for_dop[0].shape[0], for_dop[0].shape[1])))
        np.savez('./params/dop_data.npz', for_dop = for_dop)
        
        del after_window[:], for_dop[:], AIC_DATA[:], for_dop[:]
        
        
        
        '''
        debug message
        '''
        if debug_mode:
            print('GPS_rx')
            print(GPS_rx)
            print('GPS_tx')
            print(GPS_tx)
            print('v_rx')
            print(v_rx)
            print('v_tx')
            print(v_tx)
            print('rel_speed')
            print(rel_speed)
            print('ATT')
            print(ATT)
            print('T')
            print(T)
            print('d')
            print(d)
            print('win_wide')
            print(win_wide)
            print('pdp_window')
            print(pdp_window.shape)
            print(pdp_window[-1][0:6])
            print('D_window')
            print(D_window.shape)
            print(D_window[20:26])
            print('TIME')
            print(TIME.shape)
            print(TIME[20:26])
            print('V_Rel')
            print(V_Rel.shape)
            print(V_Rel[20:26])
            print('Chirp_f')
            print(Chirp_f.shape)
            print(Chirp_f[0:6])
            print('PL_no_sm')
            print(PL_no_sm.shape)
            print(PL_no_sm[0:6])
            print('SM_time')
            print(SM_time.shape)
            print(SM_time[0:6])
            print(SM_time[-6:])
            print('SM_distance')
            print(SM_distance.shape)
            print(SM_distance[0:6])
            print(SM_distance[-6:])
            print('Small_scale_fading')
            print(Small_scale_fading.shape)
            print(Small_scale_fading[0:6])
            print(Small_scale_fading[-6:])
            print('p_Hz')
            print(p_Hz.shape)
            print(p_Hz)
            print('p_De')
            print(p_De.shape)
            print(p_De)
            print('Max_doppler')
            print(Max_doppler.shape)
            print(Max_doppler)
            print('CIR_doppler')
            print(CIR_doppler.shape)
            print(CIR_doppler[0, 0:6])
            print(CIR_doppler[-1, 0:6])
            print('Fre_innor_domain')
            print(Fre_innor_domain.shape)
            print(Fre_innor_domain[0, 0:6])
            print(Fre_innor_domain[-1, 0:6])
            print('Fre_resolution')
            print(Fre_resolution)
            print('Hz_in_x')
            print(Hz_in_x.shape)
            print(Hz_in_x[0:6])
            print(Hz_in_x[-6:])
            print('channel_gain')
            print(channel_gain.shape)
            print(channel_gain[0:6])
            print(channel_gain[-6:])
            print('num_AA')
            print(num_AA.shape)
            print(num_AA)
            print('num_BB')
            print(num_BB.shape)
            print(num_BB)
            print('LOS_doppler')
            print(LOS_doppler.shape)
            print(LOS_doppler[0:6])
            print(LOS_doppler[-6:])
            print('LOS_delay')
            print(LOS_delay.shape)
            print(LOS_delay[0:6])
            print(LOS_delay[-6:])
            print('value_max')
            print(value_max)
            print('index_max')
            print(index_max)
            print('index_cut')
            print(index_cut)
            
    def xls_folder_process(self, xls_folder):
        # 遍历path目录选取所有.txt文件
        xls_list = []
        for dir_path, dir_names, file_names in os.walk(xls_folder):
            for file_name in file_names:
                if os.path.splitext(file_name)[-1] == '.xls':
                    xls_list.append(os.path.join(dir_path, file_name))
                    
        # 提取txt文件名的前一部分，这里需要保证排序的数字的前一部分必须确定，且以'_'分割
        file_header = '_'.join(os.path.splitext(xls_list[0])[0].split('_')[:-1])
        # 提取xls文件名中排序的部分，并且拼接
        rx_file = ''
        tx_file = ''
        xls_list = [os.path.splitext(file_name)[0].split('_')[-1] for file_name in xls_list]
        for i in xls_list:
            if i == 'rx' or i == 'RX' or i == 'Rx':
                rx_file = file_header + '_' + i + '.xls'
            elif i == 'tx' or i == 'TX' or i == 'Tx':
                tx_file = file_header + '_' + i + '.xls'
        print(rx_file)
        print(tx_file)
        return rx_file, tx_file
        

if __name__ == '__main__':
    begin_time = timeit.default_timer()
    
    '''
    主程序
    '''
    main_doppler()
    
    end_time = timeit.default_timer()
    print('Running time')
    print(str(end_time - begin_time))