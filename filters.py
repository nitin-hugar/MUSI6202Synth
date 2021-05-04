# Functions are all filters
import numpy as np
import math
import utils

class Filters:

    def __init__(self, data, sampling_rate):
        self.data = data
        self.sampling_rate = sampling_rate

    def biquad(self, type, gain, center_frequency, Q):

        x = utils.LinearWrap(self.data)
        output_length = len(x)+2
        y = np.zeros(output_length)

        m_fxn1 = 0.0
        m_fxn2 = 0.0
        m_fyn1 = 0.0
        m_fyn2 = 0.0

        A = math.pow(10.0, gain / 40.0)
        w0 = 2 * math.pi * (center_frequency / self.sampling_rate)
        alpha = math.sin(w0) / (2 * Q)

        if type == "lowpass":
            m_fb0 = (1 - math.cos(w0)) / 2
            m_fb1 = 1 - math.cos(w0)
            m_fb2 = (1 - math.cos(w0)) / 2
            m_fa0 = 1 + alpha
            m_fa1 = -2 * math.cos(w0)
            m_fa2 = 1 - alpha

        if type == "hipass":
            m_fb0 = (1 + math.cos(w0)) / 2
            m_fb1 = -(1 + math.cos(w0))
            m_fb2 = (1 + math.cos(w0)) / 2
            m_fa0 = 1 + alpha
            m_fa1 = -2 * math.cos(w0)
            m_fa2 = 1 - alpha

        if type == "bandpass":
            m_fb0 = alpha
            m_fb1 = 0
            m_fb2 = -1 * alpha
            m_fa0 = 1 + alpha
            m_fa1 = -2 * math.cos(w0)
            m_fa2 = 1 - alpha

        if type == "allpass":
            m_fb0 = 1 - alpha
            m_fb1 = -2 * math.cos(w0)
            m_fb2 = 1 + alpha
            m_fa0 = 1 + alpha
            m_fa1 = -2 * math.cos(w0)
            m_fa2 = 1 - alpha

        if type == "peak":
            m_fb0 = 1 + alpha * A
            m_fb1 = -2 * math.cos(w0)
            m_fb2 = 1 - alpha * A
            m_fa0 = 1 + alpha / A
            m_fa1 = -2 * math.cos(w0)
            m_fa2 = 1 - alpha / A

        if type == "notch":
            m_fb0 = 1
            m_fb1 = -2 * math.cos(w0)
            m_fb2 = 1
            m_fa0 = 1 + alpha
            m_fa1 = -2 * math.cos(w0)
            m_fa2 = 1 - alpha

        if type == "lowshelf":
            m_fb0 = A * ((A + 1) - (A - 1) * math.cos(w0) + 2 * math.sqrt(A) * alpha)
            m_fb1 = 2 * A * ((A - 1) - (A + 1) * math.cos(w0))
            m_fb2 = A * ((A + 1) - (A - 1) * math.cos(w0) - 2 * math.sqrt(A) * alpha)
            m_fa0 = (A + 1) + (A - 1) * math.cos(w0) + 2 * math.sqrt(A) * alpha
            m_fa1 = -2 * ((A - 1) + (A + 1) * math.cos(w0))
            m_fa2 = (A + 1) + (A - 1) * math.cos(w0) - 2 * math.sqrt(A) * alpha

        if type == "highshelf":
            m_fb0 = A * ((A + 1) + (A - 1) * math.cos(w0) + 2 * math.sqrt(A) * alpha)
            m_fb1 = -2 * A * ((A - 1) + (A + 1) * math.cos(w0))
            m_fb2 = A * ((A + 1) + (A - 1) * math.cos(w0) - 2 * math.sqrt(A) * alpha)
            m_fa0 = (A + 1) - (A - 1) * math.cos(w0) + 2 * math.sqrt(A) * alpha
            m_fa1 = 2 * ((A - 1) - (A + 1) * math.cos(w0))
            m_fa2 = (A + 1) - (A - 1) * math.cos(w0) - 2 * math.sqrt(A) * alpha

        for i in range(output_length):
            output_sample = (m_fb0 / m_fa0) * x[i] + (m_fb1 / m_fa0) * m_fxn1 + (m_fb2 / m_fa0) * m_fxn2 - (m_fa1 / m_fa0) * m_fyn1 - (m_fa2 / m_fa0) * m_fyn2

            m_fxn2 = m_fxn1
            m_fxn1 = x[i]
            m_fyn2 = m_fyn1
            m_fyn1 = output_sample

            y[i] = gain * output_sample

        return y