# coding=utf-8

from PyQt5.QtCore import QThread, pyqtSignal
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

        
def plot_Main_function_and_doppler_fig1():
    cache = np.load('./plot_params/Main_function_and_doppler_fig1.npz')
    TIME = cache['TIME']
    t_res = cache['t_res']
    pdp_window = cache['pdp_window']
    channel_gain = cache['channel_gain']
    
    #fig = plt.figure(figsize=(8, 6), dpi=100, tight_layout=True)
    # 自动控制排版
    fig = plt.figure(tight_layout = True)

    ax = fig.add_subplot(211)
    X, Y = np.meshgrid(TIME, np.arange(t_res, t_res * 2560 + t_res / 10e4, t_res))
    Z = 10 * np.log10(pdp_window.T)

    ax.contourf(X, Y, Z, cmap = cm.jet)
    ax.set_xlim(np.min(TIME), np.max(TIME))
    ax.set_ylim(0, t_res * 400)
    ax.set_xlabel('Time in s', fontproperties = 'Times New Roman', fontsize = 10)
    ax.set_ylabel('Delay in ns', fontproperties = 'Times New Roman', fontsize = 10)

    ax = fig.add_subplot(212)
    ax.plot(TIME, channel_gain, 'b',linewidth = 2.0)
    ax.set_xlim(np.min(TIME), np.max(TIME))
    ax.set_ylim(np.min(channel_gain), np.max(channel_gain))
    ax.set_xlabel('Time in s', fontproperties = 'Times New Roman', fontsize = 10)
    ax.set_ylabel('Channel gain in dB', fontproperties = 'Times New Roman', fontsize = 10)
    # 显示网格
    ax.grid(True)
    
    plt.show()
    return
        
def plot_Main_function_and_doppler_fig11():
    cache = np.load('./plot_params/Main_function_and_doppler_fig11.npz')
    TIME = cache['TIME']
    t_res = cache['t_res']
    pdp_window = cache['pdp_window']
    
    fig = plt.figure(tight_layout = True)
    ax = fig.add_subplot(111, projection = '3d')
    
    X, Y = np.meshgrid(TIME, np.arange(t_res, t_res * 2560 + t_res / 10e4, t_res))
    Z = 10 * np.log10(pdp_window.T)
    
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.jet, linewidth=0, antialiased=False)
    ax.view_init(None, 30)
    ax.set_xlabel('Time in s', fontproperties = 'Times New Roman', fontsize = 10)
    ax.set_zlabel('Delay in ns', fontproperties = 'Times New Roman', fontsize = 10)
    
    ax.disable_mouse_rotation()
    
    plt.show()
    return

def plot_Main_function_and_doppler_fig2():
    cache = np.load('./plot_params/Main_function_and_doppler_fig2.npz')
    X = cache['X']
    Y = cache['Y']
    t_res = cache['t_res']
    
    fig = plt.figure(tight_layout = True)
    ax = fig.add_subplot(111)
    ax.plot(X, Y, 'b', linewidth = 2)
    ax.set_xlim(0, t_res * 2560)
    ax.set_ylim(np.min(Y), np.max(Y))
    ax.set_xlabel('Time in ns', fontproperties = 'Times New Roman', fontsize = 10)
    ax.set_ylabel('Average PDP in dB', fontproperties = 'Times New Roman', fontsize = 10)
    ax.grid(True)
    
    plt.show()
    return

def plot_Main_function_and_doppler_fig3():
    cache = np.load('./plot_params/Main_function_and_doppler_fig3.npz')
    X = cache['X']
    Y = cache['Y']
    Z = cache['Z']
    
    fig = plt.figure(tight_layout = True)
    ax = fig.add_subplot(111)
    ax.contourf(X, Y, Z, cmap = cm.jet)
    ax.set_xlim(0, 5)
    ax.set_ylim(-966, 966)
    ax.set_xlabel('Time in us', fontproperties = 'Times New Roman', fontsize = 10)
    ax.set_ylabel('Doppler Frequency in Hz', fontproperties = 'Times New Roman', fontsize = 10)
    
    plt.show()
    return

def plot_Main_function_and_doppler_fig4():
    cache = np.load('./plot_params/Main_function_and_doppler_fig4.npz')
    X = cache['X']
    Y = cache['Y']
    Z = cache['Z']
    
    fig = plt.figure(tight_layout = True)
    ax = fig.add_subplot(111)
    ax.contourf(X, Y, Z, cmap = cm.jet)
    ax.set_xlim(0, 2000)
    ax.set_ylim(-966, 966)
    ax.set_xlabel('Delay in us', fontproperties = 'Times New Roman', fontsize = 10)
    ax.set_ylabel('Doppler Frequency in Hz', fontproperties = 'Times New Roman', fontsize = 10)
    
    plt.show()
    return

def plot_Main_function_and_doppler_fig5():
    cache = np.load('./plot_params/Main_function_and_doppler_fig5.npz')
    SM_time = cache['SM_time']
    NB_signal = cache['NB_signal']
    PL_no_SM = cache['PL_no_SM']
    
    fig = plt.figure(tight_layout = True)
    ax = fig.add_subplot(111)
    ax.plot(SM_time, NB_signal, 'b-')
    ax.plot(SM_time, PL_no_SM, 'r-')
    ax.set_xlabel('time in seconds', fontproperties = 'Times New Roman', fontsize = 10)
    ax.set_ylabel('RSL in dBm', fontproperties = 'Times New Roman', fontsize = 10)
    ax.grid(True)
    
    plt.show()
    return

def plot_Main_function_and_doppler_fig6():
    cache = np.load('./plot_params/Main_function_and_doppler_fig6.npz')
    X = cache['X']
    Y = cache['Y']
    
    fig = plt.figure(tight_layout = True)
    ax = fig.add_subplot(111)
    ax.plot(X, Y, 'b')
    ax.set_xlim(np.min(X), np.max(X))
    ax.set_ylim(np.min(Y), np.max(Y))
    ax.set_xlabel('time in seconds', fontproperties = 'Times New Roman', fontsize = 10)
    ax.set_ylabel('Small_scale_fading in dB', fontproperties = 'Times New Roman', fontsize = 10)
    ax.grid(True)
    
    plt.show()
    return

def plot_Main_function_and_doppler_fig8():
    cache = np.load('./plot_params/Main_function_and_doppler_fig8.npz')
    X = cache['X']
    Y = cache['Y']
    
    fig = plt.figure(tight_layout = True)
    ax = fig.add_subplot(111)
    ax.plot(X, Y, 'b')
    ax.set_xlim(np.min(X), np.max(X))
    ax.set_ylim(np.min(Y), np.max(Y))
    ax.set_xlabel('Time in s', fontproperties = 'Times New Roman', fontsize = 10)
    ax.set_ylabel('Channel gain in dB', fontproperties = 'Times New Roman', fontsize = 10)
    ax.grid(True)
    
    plt.show()
    return

def plot_rmsdelay_pathnum_analysis_main_function_fig1():
    cache = np.load('./plot_params/rmsdelay_pathnum_analysis_main_function_fig1.npz')
    X = cache['X']
    Y = cache['Y']
    
    fig = plt.figure(tight_layout = True)
    ax = fig.add_subplot(111)
    ax.plot(X, Y, 'b')
    ax.grid(True)
    
    plt.show()
    return

def plot_rmsdelay_pathnum_analysis_main_function_fig2():
    cache = np.load('./plot_params/rmsdelay_pathnum_analysis_main_function_fig2.npz')
    X = cache['X']
    Y = cache['Y']
    
    fig = plt.figure(tight_layout = True)
    ax = fig.add_subplot(111)
    ax.plot(X, Y, 'b')
    ax.grid(True)
    
    plt.show()
    return

def plot_rmsdelay_pathnum_analysis_main_function_fig3():
    cache = np.load('./plot_params/rmsdelay_pathnum_analysis_main_function_fig3.npz')
    X = cache['X']
    Y = cache['Y']
    
    fig = plt.figure(tight_layout = True)
    ax = fig.add_subplot(111)
    ax.plot(X, Y, 'b')
    ax.grid(True)
    
    plt.show()
    return

def plot_rmsdelay_pathnum_analysis_main_function_fig4():
    cache = np.load('./plot_params/rmsdelay_pathnum_analysis_main_function_fig4.npz')
    X = cache['X']
    Y = cache['Y']
    
    fig = plt.figure(tight_layout = True)
    ax = fig.add_subplot(111)
    ax.plot(X, Y, 'b')
    ax.grid(True)
    
    plt.show()
    return

def plot_rmsdop_main_function_fig3():
    cache = np.load('./plot_params/rmsdop_main_function_fig3.npz')
    TIME = cache['TIME']
    Dm = cache['Dm']
    
    fig = plt.figure(tight_layout = True)
    ax = fig.add_subplot(111)

    ax.plot(TIME, Dm, 'b', linewidth = 2)

    ax.set_xlim(np.min(TIME), np.max(TIME))
    ax.set_ylim(np.min(Dm), np.max(Dm))
    ax.set_xlabel('Time in s', fontproperties = 'Times New Roman', fontsize = 10)
    ax.set_ylabel('Mean Doppler in Hz', fontproperties = 'Times New Roman', fontsize = 10)
    ax.grid(True)
    
    plt.show()
    return

def plot_rmsdop_main_function_fig4():
    cache = np.load('./plot_params/rmsdop_main_function_fig4.npz')
    TIME = cache['TIME']
    Drms = cache['Drms']
    
    fig = plt.figure(tight_layout = True)
    ax = fig.add_subplot(111)

    ax.plot(TIME, Drms, 'b', linewidth = 2)

    ax.set_xlim(np.min(TIME), np.max(TIME))
    ax.set_ylim(np.min(Drms), np.max(Drms))
    ax.set_xlabel('Time in s', fontproperties = 'Times New Roman', fontsize = 10)
    ax.set_ylabel('RMS Doppler in Hz', fontproperties = 'Times New Roman', fontsize = 10)
    ax.grid(True)
    
    plt.show()
    return

def plot_rmsdop_main_function_fig6():
    cache = np.load('./plot_params/rmsdop_main_function_fig6.npz')
    Dm = cache['Dm']
    
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
    
    plt.show()
    return

def plot_rmsdop_main_function_fig8():
    cache = np.load('./plot_params/rmsdop_main_function_fig8.npz')
    Drms = cache['Drms']
    
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
    
    plt.show()
    return

def plot_rmsdop_main_function_fig9():
    cache = np.load('./plot_params/rmsdop_main_function_fig9.npz')
    b1 = cache['b1']
    A1 = cache['A1']
    
    fig = plt.figure(tight_layout = True)
    ax = fig.add_subplot(111)

    ax.bar(b1, A1, color = 'b', width = 6)

    ax.set_xlabel('Mean Doppler in Hz', fontproperties = 'Times New Roman', fontsize = 10)
    ax.set_ylabel('PDF of mean Doppler', fontproperties = 'Times New Roman', fontsize = 10)
    ax.grid(True)
    
    plt.show()
    return

def plot_rmsdop_main_function_fig10():
    cache = np.load('./plot_params/rmsdop_main_function_fig10.npz')
    b2 = cache['b2']
    A2 = cache['A2']
    
    fig = plt.figure(tight_layout = True)
    ax = fig.add_subplot(111)

    ax.bar(b2, A2, color = 'b', width = 6)

    ax.set_xlabel('RMS Doppler in Hz', fontproperties = 'Times New Roman', fontsize = 10)
    ax.set_ylabel('PDF of RMS Doppler', fontproperties = 'Times New Roman', fontsize = 10)
    ax.grid(True)
    
    plt.show()
    return

def plot_AIC_dis_deter_mainfunction_a_fig1():
    cache = np.load('./plot_params/AIC_dis_deter_mainfunction_a_fig1.npz')
    X = cache['X']
    p_logn = cache['p_logn']
    p_naka = cache['p_naka']
    p_rice = cache['p_rice']
    p_ray = cache['p_ray']
    p_weib = cache['p_weib']
    
    fig = plt.figure(tight_layout = True)
    ax = fig.add_subplot(111)
    
    ax.plot(X, p_logn, 'rs', linewidth = 1, label = 'denotes Lognormal')
    ax.plot(X, p_naka, 'b*', linewidth = 1, label = 'denotes Nakagami-m')
    ax.plot(X, p_rice, 'r.', linewidth = 1, label = 'denotes Rician')
    ax.plot(X, p_ray, 'g*', linewidth = 1, label = 'denotes Rayleigh')
    ax.plot(X, p_weib, 'kv', linewidth = 1, label = 'denotes Weibull')
    
    ax.set_xlim(np.min(X), np.max(X))
    ax.set_ylim(0, 1)
    ax.set_xlabel('Time in s', fontproperties = 'Times New Roman', fontsize = 10)
    ax.set_ylabel('Optimal amplitude distribution', fontproperties = 'Times New Roman', fontsize = 10)
    ax.grid(True)
    plt.legend(bbox_to_anchor=(1.0, 1), loc=1, borderaxespad=0.5)
    
    plt.show()
    return

def plot_AIC_dis_deter_mainfunction_a_fig2():
    cache = np.load('./plot_params/AIC_dis_deter_mainfunction_a_fig2.npz')
    X = cache['X']
    k_factor = cache['k_factor']
    TIME = cache['TIME']
    
    fig = plt.figure(tight_layout = True)
    ax = fig.add_subplot(111)
    
    ax.plot(X, k_factor, 'b.-', linewidth = 1)
    
    ax.set_xlim(np.min(TIME), np.max(TIME))
    ax.set_ylim(np.min(k_factor), np.max(k_factor))
    ax.set_xlabel('Time in s', fontproperties = 'Times New Roman', fontsize = 10)
    ax.set_ylabel('K-factor in dB', fontproperties = 'Times New Roman', fontsize = 10)
    ax.grid(True)
    
    plt.show()
    return

def plot_AIC_dis_deter_mainfunction_a_fig3():
    cache = np.load('./plot_params/AIC_dis_deter_mainfunction_a_fig3.npz')
    X = cache['X']
    RHO = cache['RHO']
    SIGMA = cache['SIGMA']
    TIME = cache['TIME']
    
    fig = plt.figure(tight_layout = True)
    ax = fig.add_subplot(111)

    ax.plot(X, RHO, 'b.', linewidth = 1.5, label = 'RHO')
    ax.plot(X, SIGMA, 'r.', linewidth = 1.5, label = 'SIGMA')

    ax.set_xlim(np.min(TIME), np.max(TIME))
    ax.set_ylim(min(np.min(RHO), np.min(SIGMA)), max(np.max(RHO), np.max(SIGMA)))
    ax.set_xlabel('Time in s', fontproperties = 'Times New Roman', fontsize = 10)
    ax.set_ylabel('RHO & SIGMA', fontproperties = 'Times New Roman', fontsize = 10)
    ax.grid(True)
    plt.legend(bbox_to_anchor=(1.0, 1), loc=1, borderaxespad=0.5)
    
    plt.show()
    return

def plot_AIC_dis_deter_mainfunction_a_fig4():
    cache = np.load('./plot_params/AIC_dis_deter_mainfunction_a_fig4.npz')
    X = cache['X']
    MU = cache['MU']
    
    fig = plt.figure(tight_layout = True)
    ax = fig.add_subplot(111)
    
    ax.plot(X, MU, 'b.', linewidth = 1.5)
    
    ax.set_xlabel('Time in s', fontproperties = 'Times New Roman', fontsize = 10)
    ax.set_ylabel('The magnitude of m-factor', fontproperties = 'Times New Roman', fontsize = 10)
    ax.grid(True)
    
    plt.show()
    return

def plot_AIC_dis_deter_mainfunction_a_fig5():
    cache = np.load('./plot_params/AIC_dis_deter_mainfunction_a_fig5.npz')
    X = cache['X']
    Weibull_a = cache['Weibull_a']
    Weibull_b = cache['Weibull_b']
    TIME = cache['TIME']
    
    fig = plt.figure(tight_layout = True)
    ax = fig.add_subplot(111)
    
    ax.plot(X, Weibull_a, 'ko', linewidth = 1, label = 'Scale parameter')
    ax.plot(X, Weibull_b, 'rp', linewidth = 1, label = 'Shape parameter')
    
    ax.set_xlim(np.min(TIME), np.max(TIME))
    ax.set_ylim(min(np.min(Weibull_a), np.min(Weibull_b)), max(np.max(Weibull_a), np.max(Weibull_b)))
    ax.set_xlabel('Time in s', fontproperties = 'Times New Roman', fontsize = 10)
    ax.set_ylabel('Magnitude', fontproperties = 'Times New Roman', fontsize = 10)
    ax.grid(True)
    plt.legend(bbox_to_anchor=(1.0, 1), loc=1, borderaxespad=0.5)
    
    plt.show()
    return

def plot_Propagation_path_loss_mainfunction_fig1():
    cache = np.load('./plot_params/Propagation_path_loss_mainfunction_fig1.npz')
    M_distance = cache['M_distance']
    PL = cache['PL']
    One_slope = cache['One_slope']
    REL = cache['REL']
    Free_space = cache['Free_space']
    WINNER_B1 = cache['WINNER_B1']
    WINNER_C2 = cache['WINNER_C2']
    ITU_R_u = cache['ITU_R_u']
    ITU_R_l = cache['ITU_R_l']
    ITU_R_m = cache['ITU_R_m']
    
    fig = plt.figure(tight_layout = True)
    ax = fig.add_subplot(111)

    ax.plot(M_distance, PL, 'b.', linewidth = 1.5, label = 'Measurement data')
    ax.plot(M_distance, One_slope, 'r-', linewidth = 1.5, label = 'One-slope model')
    ax.plot(M_distance, REL, 'c-', linewidth = 1.5, label = 'REL model')
    ax.plot(M_distance, Free_space, 'k--', linewidth = 1.5, label = 'Free-space model')
    ax.plot(M_distance, WINNER_B1, 'k-', linewidth = 1.5, label = 'WINNER II-B1')
    ax.plot(M_distance, WINNER_C2, 'g-', linewidth = 1.5, label = 'WINNER II-C2')
    ax.plot(M_distance, ITU_R_u, 'g--', linewidth = 1.5, label = 'ITU-R 1411(upper bound)')
    ax.plot(M_distance, ITU_R_l, 'r-.', linewidth = 1.5, label = 'ITU-R 1411(lower bound)')
    ax.plot(M_distance, ITU_R_m, 'b-.', linewidth = 1.5, label = 'ITU-R 1411(average value)')

    ax.set_xlabel('Distance in m', fontproperties = 'Times New Roman', fontsize = 8)
    ax.set_ylabel('Propagation path loss in dB', fontproperties = 'Times New Roman', fontsize = 8)
    ax.grid(True)
    plt.legend(bbox_to_anchor=(0, 1), loc='upper left', borderaxespad=0.5)
    
    plt.show()
    return

def plot_small_scale_fading_mainfunction_fig1():
    cache = np.load('./plot_params/small_scale_fading_mainfunction_fig1.npz')
    T = cache['T']
    RSL_all = cache['RSL_all']
    RSL_n_ssf = cache['RSL_n_ssf']
    SSF = cache['SSF']
    
    fig = plt.figure(tight_layout = True)

    ax = fig.add_subplot(211)
    ax.plot(T, RSL_all, 'b')
    ax.plot(T, RSL_n_ssf, 'g')
    ax.grid(True)

    ax = fig.add_subplot(212)
    ax.plot(T, SSF, 'b')
    ax.grid(True)
    
    plt.show()
    return

def plot_small_scale_fading_mainfunction_fig2():
    cache = np.load('./plot_params/small_scale_fading_mainfunction_fig2.npz')
    Dis = cache['Dis']
    RSL_all = cache['RSL_all']
    RSL_n_ssf = cache['RSL_n_ssf']
    SSF = cache['SSF']
    
    fig = plt.figure(tight_layout = True)

    ax = fig.add_subplot(211)
    ax.plot(Dis, RSL_all, 'b')
    ax.plot(Dis, RSL_n_ssf, 'g')
    ax.grid(True)

    ax = fig.add_subplot(212)
    ax.plot(Dis, SSF, 'b')
    ax.grid(True)
    
    plt.show()
    return

def plot_small_scale_fading_mainfunction_fig3():
    cache = np.load('./plot_params/small_scale_fading_mainfunction_fig3.npz')
    Dis = cache['Dis']
    RSL_all = cache['RSL_all']
    
    fig = plt.figure(tight_layout = True)

    ax = fig.add_subplot(111)
    ax.plot(Dis, RSL_all, 'b', linewidth = 2.0)
    ax.set_xlabel('Distance in m', fontproperties = 'Times New Roman', fontsize = 8)
    ax.set_ylabel('Received signal level in dBm', fontproperties = 'Times New Roman', fontsize = 8)
    ax.grid(True)
    
    plt.show()
    return

def plot_small_scale_fading_mainfunction_fig4():
    cache = np.load('./plot_params/small_scale_fading_mainfunction_fig4.npz')
    T = cache['T']
    RSL_all = cache['RSL_all']
    RSL_n_ssf = cache['RSL_n_ssf']
    
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
    
    plt.show()
    return

def plot_small_scale_fading_mainfunction_fig5():
    cache = np.load('./plot_params/small_scale_fading_mainfunction_fig5.npz')
    T = cache['T']
    SSF = cache['SSF']
    
    fig = plt.figure(tight_layout = True)
    ax = fig.add_subplot(111)

    ax.plot(T, SSF, 'b', linewidth = 1.5)

    ax.set_xlim(np.min(T), np.max(T))
    ax.set_ylim(np.min(SSF), np.max(SSF))
    ax.set_xlabel('Time in s', fontproperties = 'Times New Roman', fontsize = 10)
    ax.set_ylabel('Small scale fading in dB', fontproperties = 'Times New Roman', fontsize = 10)
    ax.grid(True)
    
    plt.show()
    return

def plot_small_scale_fading_mainfunction_fig6():
    cache = np.load('./plot_params/small_scale_fading_mainfunction_fig6.npz')
    lowess_LCR_per_second = cache['lowess_LCR_per_second']
    LCR_per_second = cache['LCR_per_second']
    
    fig = plt.figure(tight_layout = True)
    ax = fig.add_subplot(111)
    
    ax.plot(lowess_LCR_per_second[:, 0], lowess_LCR_per_second[:, 1], 'b', linewidth = 1.5)

    ax.set_xlim(-0.5, 0.5)
    ax.set_ylim(np.min(LCR_per_second), np.max(LCR_per_second))
    ax.set_xlabel('Threshold in dB', fontproperties = 'Times New Roman', fontsize = 10)
    ax.set_ylabel('LCR (times per second)', fontproperties = 'Times New Roman', fontsize = 10)
    ax.grid(True)
    
    plt.show()
    return

def plot_small_scale_fading_mainfunction_fig7():
    cache = np.load('./plot_params/small_scale_fading_mainfunction_fig7.npz')
    lowess_AFD = cache['lowess_AFD']
    AFD = cache['AFD']
    
    fig = plt.figure(tight_layout = True)
    ax = fig.add_subplot(111)
    
    ax.plot(lowess_AFD[:, 0], lowess_AFD[:, 1], 'b', linewidth = 1.5)

    ax.set_xlim(-0.5, 0.5)
    ax.set_ylim(np.min(AFD), np.max(AFD))
    ax.set_xlabel('Threshold in dB', fontproperties = 'Times New Roman', fontsize = 10)
    ax.set_ylabel('ADF (seconds)', fontproperties = 'Times New Roman', fontsize = 10)
    ax.grid(True)
    
    plt.show()
    return

def plot_small_scale_fading_mainfunction_fig8():
    cache = np.load('./plot_params/small_scale_fading_mainfunction_fig8.npz')
    SSF = cache['SSF']
    
    fig = plt.figure(tight_layout = True)
    ax = fig.add_subplot(111)

    ax.plot(SSF, 'b', linewidth = 1.5)
    
    plt.show()
    return

