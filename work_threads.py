# coding=utf-8

from PyQt5.QtCore import QThread, pyqtSignal

from Main_function_and_doppler.Main_function_and_doppler import main_doppler
from delay_analysis.rmsdelay_pathnum_analysis_main_function import rmsdelay_pathnum_analysis
from Doppler_analysis.rmsdop_main_function import rmsdop
from AIC_Amp_determination.AIC_dis_deter_mainfunction_a import AIC_Amp_determination
from path_loss.Propagation_path_loss_mainfunction import Propagation_path_loss
from power_domain.small_scale_fading_mainfunction import small_scale_fading

class main_doppler_thread(QThread):
    '''
    sin_out用于与UI线程的交互
    '''
    sin_out = pyqtSignal(str)
    
    def __init__(self, **kwargs):
        super(main_doppler_thread, self).__init__()
        self.working = True
        
        self.t_start = kwargs['t_start']
        self.window = kwargs['window']
        self.TX_power = kwargs['TX_power']
        self.TX_Gain = kwargs['TX_Gain']
        self.RX_Gain = kwargs['RX_Gain']
        self.TX_heigh = kwargs['TX_heigh']
        self.RX_heigh = kwargs['RX_heigh']
        self.fc = kwargs['fc']
        self.ATT_mark = kwargs['ATT_mark']
        self.cable = kwargs['cable']
        self.chirp_num = kwargs['chirp_num']
        self.txt_folder = kwargs['txt_folder']
        self.xls_folder = kwargs['xls_folder']
        
    def __del__(self):
        self.working = False
    
    def run(self):
        try:
            main_doppler(t_start = self.t_start, window = self.window, TX_power = self.TX_power, TX_Gain = self.TX_Gain, 
                         RX_Gain = self.RX_Gain,TX_heigh = self.TX_heigh, RX_heigh = self.RX_heigh, 
                         fc = self.fc, ATT_mark = self.ATT_mark, cable = self.cable, chirp_num = self.chirp_num, 
                         txt_folder = self.txt_folder, xls_folder = self.xls_folder)
        except:
            self.sin_out.emit('Main Doppler Error')
            return
        self.sin_out.emit('Main Doppler Done')
        return
        
class delay_domain_thread(QThread):
    '''
    sin_out用于与UI线程交互
    '''
    sin_out = pyqtSignal(str)
    
    def __init__(self, **kwargs):
        super(delay_domain_thread, self).__init__()
        self.working = True
        
    def __del__(self):
        self.working = False
        
    def run(self):
        rmsdelay_pathnum_analysis()
        self.sin_out.emit('Delay Domain Done')
        
class frequency_domain_thread(QThread):
    '''
    sin_out用于与UI线程交互
    '''
    sin_out = pyqtSignal(str)
    
    def __init__(self, **kwargs):
        super(frequency_domain_thread, self).__init__()
        self.working = True
        
    def __del__(self):
        self.working = False
        
    def run(self):
        rmsdop()
        self.sin_out.emit('Frequency Domain Done')
        
class power_domain_thread(QThread):
    '''
    sin_out用于与UI线程交互
    '''
    sin_out = pyqtSignal(str)
    
    def __init__(self, params_dict):
        super(power_domain_thread, self).__init__()
        self.working = True
        
        self.path_loss_polar = params_dict['path_loss_polar']
        self.path_loss_dielectric = params_dict['path_loss_dielectric']
        self.small_scale_beg_point = params_dict['small_scale_beg_point']
        self.small_scale_end_point = params_dict['small_scale_end_point']
        self.small_scale_beg_ssf_point = params_dict['small_scale_beg_ssf_point']
        self.small_scale_end_ssf_point = params_dict['small_scale_end_ssf_point']
        
        
    def __del__(self):
        self.working = False
        
    def run(self):
        AIC_Amp_determination()
        Propagation_path_loss(path_loss_polar = self.path_loss_polar, path_loss_dielectric = self.path_loss_dielectric)
        small_scale_fading(small_scale_beg_point = self.small_scale_beg_point, small_scale_end_point = self.small_scale_end_point,
                           small_scale_beg_ssf_point = self.small_scale_beg_ssf_point, small_scale_end_ssf_point = self.small_scale_end_ssf_point)
        self.sin_out.emit('Power Domain Done')
    