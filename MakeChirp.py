# coding=utf-8
import numpy as np

def MakeChirp(SampFreqDec, ChirpBandw, NchirpDec):
    fs = SampFreqDec                                                    # 采样频率=1/delay_resolution
    fc = 0                                                              # 基带信号不需要加入2.075 GHz和载波无关
    B = ChirpBandw                                                      # 带宽100MHz
    N = NchirpDec                                                       # 每个chirp的sample数
    
    tmp = N * (fc - 0.5 * B) / fs
    ko = np.floor(tmp + 0.5) / N
    tmp2 = 0.5 * N * B / fs
    kc = np.floor(tmp2 + 0.5) / (N * N)
    ch = np.zeros((1, N))
    
    i = np.linspace(0, N-1, N)
    ii = i * i
    pi2 = np.pi * 2
    ch = np.exp(pi2 * np.complex('0+1j') * (ko * i + kc * ii))
    
    return ch

if __name__ == '__main__':
    Chirp_t = MakeChirp(SampFreqDec = 1 / 8.125e-9, ChirpBandw = 100e6, NchirpDec = 2560)
    print('Chirp_t')
    print(Chirp_t.shape)
    print(Chirp_t[0:6])
    
