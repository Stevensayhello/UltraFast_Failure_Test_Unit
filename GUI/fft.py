# FFT
import scipy
import scipy.fftpack
from scipy.fft import fft, fftfreq , rfft, rfftfreq
import numpy as np
import matplotlib.pyplot as plt

'''
def GetFFT(data, time):
            # normalization
            normalized_data = np.int16((data / data.max()) * 32767) #
            period = time[1] - time[0]
            # Number of samples in normalized_tone
            N = len(data)
            yf = fft(normalized_data)
            xf = fftfreq(N, period)
            
            XF = np.array(xf)
            YF = np.array(yf)
            #get max frequency
            list_a = YF.tolist()
            list_a_max_list = max(list_a)  # 返回最大值
            max_index = list_a.index(max(list_a))  # 返回最大值的索引
            max_freq = XF[max_index]
            return xf , yf, max_freq
'''

def GetFFTdB(data,time):

    N = len(data)
    Ts = time[1] - time[0]  # sampling interval in time
    sample_freq =  1 / Ts #sampling freq in Hz
    secs = time.max()

    ref = 32768

    win = np.hamming(N)

    x = data[0:N] * win
    #normalized_data = np.int16(( x/ x.max()) * 32767)
    sp = np.fft.rfft(x)                               # Calculate real FFT

    s_mag = np.abs(sp) * 2 / np.sum(win)

    s_dbfs = 20 * np.log10(s_mag / ref)  # Convert to dBFS

    if (N % 2) == 0:
        freq = np.arange((float(N)/2)+1)/(float(N)/sample_freq)  # Frequency axis
    else:
        freq = np.arange(float(N)/2)/(float(N)/sample_freq)  # Frequency axis

    # get max frequency
    list_a = s_dbfs.tolist()
    list_a_max_list = max(list_a)  # return max
    max_index = list_a.index(max(list_a))  # return Max index
    max_freq = freq[max_index]

    return freq, s_dbfs, max_freq

