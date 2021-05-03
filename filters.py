# Functions are all filters
import numpy as np
import math
import utils

class Filters:

    def __init__(self, data, sampling_rate):
        self.data = data
        self.sampling_rate = sampling_rate

    def biquad(self, type="lowpass", resonance=0.2, cutoff_frequency=1000):

        x = utils.LinearWrap(self.data)

        maxDelaySamps = 2  # Only need last two samples for second order biquad
        outputSamps = len(x) + maxDelaySamps
        y = np.zeros(outputSamps)
        ringBuf = utils.LinearRingBuffer(maxDelaySamps)

        if type == "lowpass":
            c = 1.0 / math.tan(math.pi * cutoff_frequency / self.sampling_rate)

            a1 = 1.0 / (1.0 + resonance * c + c * c)
            a2 = 2 * a1
            a3 = a1
            b1 = 2.0 * (1.0 - c * c) * a1
            b2 = (1.0 - resonance * c + c * c) * a1

        if type == "hipass":
            c = math.tan(math.pi * cutoff_frequency / self.sampling_rate)

            a1 = 1.0 / (1.0 + resonance * c + c * c)
            a2 = -2 * a1
            a3 = a1
            b1 = 2.0 * (c * c - 1.0) * a1
            b2 = (1.0 - resonance * c + c * c) * a1

        for i in range(outputSamps):
            s = x[i]
            ringBuf.pushSample(s)
            y[i] = s * BL + ringBuf.delayedSample(delaySamps) * FF

            phi = phi + deltaPhi
            while phi >= 1:
                phi -= 1