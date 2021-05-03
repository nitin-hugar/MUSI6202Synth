# Post processing scripts: interpolation, dithering, resampling and output

from scipy import signal
import numpy as np
import soundfile as sf
from scipy.interpolate import interp1d
import wavio

"""
To Do: 
1. Make plots for all the outputs. 
2. Down Quantization function
"""


class Downsampler:
    def __init__(self):
        self.output_fs = int(48000)
        self.output_br = int(32)

    def write_wav(self, wave_file_path, data, fs=int(48000), bitrate=int(32)):
        print("writing data:", data, "sampling-rate:", fs, "at bit-rate:", bitrate, " to ", wave_file_path)
        if bitrate == 8:
            sampwidth = 1
        elif bitrate == 16:
            sampwidth = 2
        elif bitrate == 24:
            sampwidth = 3
        else:
            sampwidth = 4
        wavio.write(wave_file_path, data, fs, sampwidth=sampwidth)

    def low_pass(self, data, target_fs, source_fs):
        b, a = signal.butter(N=2, Wn=target_fs / 2, btype='low', analog=False, fs=source_fs)
        filtered = signal.filtfilt(b, a, data)
        return filtered

    def down_sample(self, data, factor, target_fs, source_fs):
        filtered_data = self.low_pass(data, target_fs, source_fs)
        return filtered_data[::factor]

    def cubic_interpolate(self, data, t, num_samples):
        x = np.linspace(0, t, num=len(data), endpoint=True)
        y = data
        interpolate = interp1d(x, y, kind='cubic')
        x2 = np.linspace(0, t, num=num_samples, endpoint=True)
        return interpolate(x2)

    def up_sample(self, data, source_fs, target_fs, t):
        new_samples = int(int(len(data) / source_fs) * int(target_fs))
        return self.cubic_interpolate(data, t, new_samples)

    def add_triangular_dither(self, data, old_br, new_br):
        diff = old_br - new_br
        left = (-1) * (2 ** diff)
        mode = 0
        right = (2 ** diff) - 1
        size = data.shape
        noise = np.random.triangular(left, mode, right, size)
        noise = noise.astype(np.int32)

        return data + noise

    def down_quantization(self, data, old_br, new_br):
        dithered = self.add_triangular_dither(data, old_br, new_br)
        dithered = dithered.astype(np.int32)
        down_quantized = np.zeros(len(dithered), dtype=np.int32)

        for i in range(len(dithered)):
            down_quantized[i] = dithered[i] >> (old_br - new_br)
        return down_quantized
