# Generator functions for sq, sine, saw, tri waves
import numpy as np
import ADSR

class Generators:
    def __init__(self, notes, fs):
        self.frequencies = notes.frequencies
        self.durations = notes.durations
        self.fs = fs
        self.amplitude = 1
        self.numOfNotes = len(notes.frequencies)


    def make_sound(self, envelope, partials, coefficients):
        sound = []

        # for i in np.arange(self.numOfNotes):
        #     omega = 2 * np.pi * self.frequencies[i]
        #     t = np.arange(0, float(self.durations[i]), float(1 / self.fs))
        #     signal = 0
        #     for k in range(0, len(partials)):
        #         signal += (1/partials[k]) * np.sin(k * omega * t)
        #         x = self.amplitude * coefficients[k] * (4/np.pi) * signal
        #         env = ADSR.getadsr(x, envelope)
        #         x_env = x * env[:len(x)]
        #         sound.extend(x_env)

        for i in range(self.numOfNotes):
            omega = 2 * np.pi * self.frequencies[i]
            t = np.arange(0, float(self.durations[i]), float(1/self.fs))
            x = self.amplitude * np.sin(omega * t)
            env = ADSR.getadsr(x, envelope)
            x_env = x * env[:len(x)]
            sound.extend(x_env)
        return np.array(sound)


            
            # if signalType == 'sine':
            #     x = self.amplitude * np.sin(omega * t)
            #     env = ADSR.getadsr(x, envelope)
            #     x_env = x * env[:len(x)]
            #     sound.extend(x_env)

            # elif signalType == 'square':
            #     square = 0
            #     for k in np.arange(1, numOfHarmonics, 2):
            #         square += (1/k) * np.sin(k * omega * t)
            #         x = self.amplitude * (4/np.pi)*square
            #         env = ADSR.getadsr(x, envelope)
            #         x_env = x * env[:len(x)]
            #     sound.extend(x_env)

            # elif signalType == 'sawtooth':
            #     saw = 0
            #     for k in range(1,numOfHarmonics):
            #         saw += (np.power(-1, k)) * (np.sin(omega * k * t)) / k
            #         x = (2 * self.amplitude / np.pi) * saw
            #         env = ADSR.getadsr(x, envelope)
            #         x_env = x * env[:len(x)]
            #     sound.extend(x_env)

        # return np.array(sound)




