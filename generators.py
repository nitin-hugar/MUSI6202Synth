# Generator functions for sq, sine, saw, tri waves
import numpy as np
#import matplotlib.pyplot as plt

class Generators:
    def __init__(self, notes, fs):
        self.frequencies = notes.frequencies
        self.durations = notes.durations
        self.fs = fs
        self.amplitude = 0.8
        self.numOfNotes = len(notes.frequencies)

    def make_sound(self, signalType, numOfHarmonics):
        sound = []
        for i in np.arange(self.numOfNotes):
            omega = 2 * np.pi * self.frequencies[i]
            t = np.arange(0, self.durations[i], float(1 / self.fs))

            if signalType == 'sine':
                sound.extend(self.amplitude * np.sin(omega * t))

            elif signalType == 'square':
                square = 0
                for k in np.arange(1,numOfHarmonics,2):
                    square += (1/k)* np.sin(k * omega * t)
                sound.extend((4/np.pi)*square)

            elif signalType == 'sawtooth':
                saw = 0
                for k in range(1,numOfHarmonics):
                    saw += (np.power(-1, k)) * (np.sin(omega * k * t)) / k
                sound.extend((2 * self.amplitude / np.pi) * saw)

            # elif signalType == 'triangle':
            #     triangle = 0
            #     for k in np.arange(1, numOfHarmonics):
            #         n = float((2*k) + 1)
            #         triangle += (np.power(-1, k)) * np.power(n, -2) * np.sin(omega * n * t)
            #
            #     sound.extend((8 / np.pi ** 2) * triangle)
            # plt.plot(triangle)
            # plt.show()

        return np.array(sound)

