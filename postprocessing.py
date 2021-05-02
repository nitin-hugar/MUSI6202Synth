# Post processing scripts: interpolation, dithering, resampling and output

from scipy import signal
import numpy as np
import soundfile as sf
from scipy.interpolate import interp1d
from subtype import Subtype

"""
To Do: 
1. Make plots for all the outputs. 
2. Down Quantization function
"""

def write_wav(wave_file_path, data, fs=int(48000), bitrate=int(32)):
    subtype = Subtype().get_subtype(bitrate)
    sf.write(wave_file_path, data, fs, subtype=subtype)

def low_pass(data, target_fs, source_fs):
    b, a = signal.butter(N=2, Wn=target_fs / 2, btype='low', analog=False, fs=source_fs)
    filtered = signal.filtfilt(b, a, data)
    return filtered

def down_sample(data, factor, target_fs, source_fs):
    filtered_data = low_pass(data, target_fs, source_fs)
    return filtered_data[::factor]

def cubic_interpolate(data, t, num_samples):
    x = np.linspace(0, t, num=len(data), endpoint=True)
    y = data
    interpolate = interp1d(x, y, kind='cubic')
    x2 = np.linspace(0, t, num=num_samples, endpoint=True)
    return interpolate(x2)

def up_sample(data, source_fs, target_fs, t):
    new_samples = int(int(len(data) / source_fs) * int(target_fs))
    return cubic_interpolate(data, t, new_samples)

def add_dither(data):
    noise = np.random.normal(0, .01, data.shape)
    return data + noise
