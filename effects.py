# Functions to produce effects

import numpy as np
import math
from scipy.signal import fftconvolve
import soundfile as sf


class RingBuffer(object):
    def __init__(self, maxDelay):
        self.maxDelay = maxDelay + 1
        self.buf = np.zeros(self.maxDelay)
        self.writeInd = 0

    def pushSample(self, s):
        self.buf[self.writeInd] = s
        self.writeInd = (self.writeInd + 1) % len(self.buf)

    def delayedSample(self, d):
        d = min(self.maxDelay - 1, max(0, d))
        i = ((self.writeInd + self.maxDelay) - d) % self.maxDelay
        return self.buf[i]


# Linear Interpolation
class LinearWrap(object):
    def __init__(self, it):
        self.it = it

    def __len__(self):
        return len(self.it)

    def __setitem__(self, inI, val):
        if type(inI) != int:
            raise RuntimeError('Can only write to integer values')
        self.it[inI] = val

    def __getitem__(self, inI):
        loI = math.floor(inI)
        hiI = math.ceil(inI)
        a = inI - loI
        inRange = lambda val: val >= 0 and val < len(self.it)
        loX = self.it[loI] if inRange(loI) else 0
        hiX = self.it[hiI] if inRange(hiI) else 0
        return loX * (1 - a) + hiX * a


# Wrap inner iterable inside RingBuffer with float indexable array
class LinearRingBuffer(RingBuffer):
    def __init__(self, maxDelay):
        self.maxDelay = maxDelay + 1
        self.buf = LinearWrap(np.zeros(self.maxDelay))
        self.writeInd = 0


class Effects:
    def __init__(self, data, sampling_rate):
        self.data = data
        self.sampling_rate = sampling_rate

    def chorus(self, fmod=1.5, A=0.002, M=0.002, BL=1.0, FF=0.7):

        # Simple Chorus
        x = LinearWrap(self.data)
        A = int(A * self.sampling_rate)
        M = int(M * self.sampling_rate)

        if A > M:
            raise RuntimeError("Amplitude of vibrato too high for delay length")

        maxDelaySamps = M + A + 2  # Probably don't need the 2 here, but being safe
        outputSamps = len(x) + maxDelaySamps
        y = np.zeros(outputSamps)
        ringBuf = LinearRingBuffer(maxDelaySamps)
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

        return y

    # Simple Flanger
    def flanger(self):

        x = LinearWrap(self.data)

        fmod = 0.2
        A = int(0.002 * self.sampling_rate)
        M = int(0.002 * self.sampling_rate)
        BL = 0.7
        FF = 0.7

        if A > M:
            raise RuntimeError("Amplitude of vibrato too high for delay length")

        maxDelaySamps = M + A + 2  # Probably don't need the 2 here, but being safe
        outputSamps = len(x) + maxDelaySamps
        y = np.zeros(outputSamps)
        ringBuf = LinearRingBuffer(maxDelaySamps)
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

        return y

    # Modulated Echo (Vibrato)
    def vibrato(self):

        x = LinearWrap(self.data)

        maxDelaySamps = 200
        outputSamps = len(x) + maxDelaySamps
        y = np.zeros(outputSamps)
        ringBuf = LinearRingBuffer(maxDelaySamps)

        fmod = 1
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

        return y

    # Simple Echo
    def echo(self):

        x = LinearWrap(self.data)

        output = '../output/sv_simpleEcho2.wav'

        fmod = 0
        A = 0
        M = int(0.05 * self.sampling_rate)
        BL = 0.7
        FF = 0.7

        if A > M:
            raise RuntimeError("Amplitude of vibrato too high for delay length")

        maxDelaySamps = M + A + 2  # Probably don't need the 2 here, but being safe
        outputSamps = len(x) + maxDelaySamps
        y = np.zeros(outputSamps)
        ringBuf = LinearRingBuffer(maxDelaySamps)
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

        return y

    def conv_reverb(self, impulse_path, amount_verb=0.2):

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

        return dry_signal + wet_signal + x_zp

