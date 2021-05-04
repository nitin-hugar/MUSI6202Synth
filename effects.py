# Functions to produce effects

import numpy as np
import math
import soundfile as sf
import utils
from filters import *


class Effects:
    def __init__(self, data, sampling_rate):
        self.data = data
        self.sampling_rate = sampling_rate

    def chorus(self, fmod=1.5, A=0.002, M=0.002, BL=1.0, FF=0.7):
        """

        :param fmod: frequency modulation
        :param A: amplitude of modulation
        :param M: delay time
        :param BL: blend
        :param FF: feed forward
        :return: data with chorus added
        """

        # Simple Chorus
        x = utils.LinearWrap(self.data)
        A = int(A * self.sampling_rate)
        M = int(M * self.sampling_rate)

        if A > M:
            raise RuntimeError("Amplitude of vibrato too high for delay length")

        maxDelaySamps = M + A + 2
        outputSamps = len(x) + maxDelaySamps
        y = np.zeros(outputSamps)
        ringBuf = utils.LinearRingBuffer(maxDelaySamps)
        deltaPhi = fmod / self.sampling_rate
        phi = 0

        for i in range(outputSamps):
            s = x[i]
            ringBuf.pushSample(s)
            delaySamps = M + int(math.sin(2 * math.pi * phi) * A)
            y[i] = s * BL + ringBuf.delayedSample(delaySamps) * FF

            phi = phi + deltaPhi
            while phi >= 1:
                phi -= 1

        self.data = y

    # Simple Flanger
    def flanger(self, fmod=0.2, A=0.002, M=0.002, BL=0.7, FF=0.7):
        """

           :param fmod: frequency modulation
           :param A: amplitude of modulation
           :param M: delay time
           :param BL: blend
           :param FF: feed forward
           :return: data with flanger added
         """

        x = utils.LinearWrap(self.data)

        A = int(A * self.sampling_rate)
        M = int(M * self.sampling_rate)

        if A > M:
            raise RuntimeError("Amplitude of vibrato too high for delay length")

        maxDelaySamps = M + A + 2
        outputSamps = len(x) + maxDelaySamps
        y = np.zeros(outputSamps)
        ringBuf = utils.LinearRingBuffer(maxDelaySamps)
        deltaPhi = fmod / self.sampling_rate
        phi = 0

        for i in range(outputSamps):
            s = x[i]
            ringBuf.pushSample(s)
            delaySamps = M + int(math.sin(2 * math.pi * phi) * A)
            y[i] = s * BL + ringBuf.delayedSample(delaySamps) * FF

            phi = phi + deltaPhi
            while phi >= 1:
                phi -= 1

        self.data = y

    # Modulated Echo (Vibrato)
    def vibrato(self,  maxDelaySamps=200, fmod=1):

        """

        :param maxDelaySamps: maximum delay samples
        :param fmod: frequency modulation
        :return: data with vibrato added
        """

        x = utils.LinearWrap(self.data)

        outputSamps = len(x) + maxDelaySamps
        y = np.zeros(outputSamps)
        ringBuf = utils.LinearRingBuffer(maxDelaySamps)

        deltaPhi = fmod / self.sampling_rate
        phi = 0

        for i in range(outputSamps):
            s = x[i]
            ringBuf.pushSample(s)
            delaySamps = int((math.sin(2 * math.pi * phi) + 1.001) * maxDelaySamps)
            y[i] = ringBuf.delayedSample(delaySamps) * 0.5

            phi = phi + deltaPhi
            while phi >= 1:
                phi -= 1

        self.data = y

    # Simple Echo
    def echo(self, fmod=0, A=0, M=0.05, BL=0.7, FF=0.7):
        """
           :param fmod: frequency modulation
           :param A: amplitude of modulation
           :param M: delay time
           :param BL: blend
           :param FF: feed forward
           :return: data with chorus added
         """

        x = utils.LinearWrap(self.data)
        M = int(M * self.sampling_rate)

        if A > M:
            raise RuntimeError("Amplitude of vibrato too high for delay length")

        maxDelaySamps = M + A + 2  # Probably don't need the 2 here, but being safe
        outputSamps = len(x) + maxDelaySamps
        y = np.zeros(outputSamps)
        ringBuf = utils.LinearRingBuffer(maxDelaySamps)
        deltaPhi = fmod / self.sampling_rate
        phi = 0

        for i in range(outputSamps):
            s = x[i]
            ringBuf.pushSample(s)
            delaySamps = M + int(math.sin(2 * math.pi * phi) * A)
            y[i] = s * BL + ringBuf.delayedSample(delaySamps) * FF

            phi = phi + deltaPhi
            while phi >= 1:
                phi -= 1

        self.data = y

    def conv_reverb(self, impulse_path, amount_verb=0.4):

        impulse = sf.read(impulse_path, self.sampling_rate)[0]
        impulse = impulse[:, 0]
        dry_signal = self.data
        L, P = len(self.data), len(impulse)
        h_zp = np.append(impulse, np.zeros(L-1))
        x_zp = np.append(dry_signal, np.zeros(P-1))
        X = np.fft.fft(x_zp)

        convolved_wave = np.fft.ifft(X * np.fft.fft(h_zp)).real
        wet_signal = (convolved_wave / np.abs(np.max(convolved_wave))) * amount_verb

        if len(dry_signal) < len(wet_signal):
            pad_length = np.abs(len(dry_signal) - len(wet_signal))
            dry_signal = np.pad(dry_signal, (0, pad_length), 'constant')
        elif len(wet_signal) < len(dry_signal):
            pad_length = np.abs(len(dry_signal) - len(wet_signal))
            wet_signal = np.pad(wet_signal, (0, pad_length), 'constant')

        self.data = dry_signal + wet_signal + x_zp

    def filters(self, type="lowpass", gain=1.0, center_frequency=100, Q=0.8):
        filter = Filters(self.data, self.sampling_rate)
        self.data = filter.biquad(type, gain, center_frequency, Q)

