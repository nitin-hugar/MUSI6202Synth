# Generator functions for sq, sine, saw, tri waves
import numpy as np
import ADSR
from utils import LinearWrap

class Generators:
    def __init__(self, notes, fs):
        self.notenumbers = notes.notenumbers
        self.frequencies = notes.frequencies
        self.durations = notes.durations
        self.fs = fs
        self.amplitude = 0.4
        self.numOfNotes = len(notes.frequencies)


    def additive(self, envelope, partials, coefficients):
        sound = []
        for i in np.arange(self.numOfNotes):
            omega = 2 * np.pi * self.frequencies[i]
            t = np.arange(0, float(self.durations[i]), float(1 / self.fs))
            signal = 0
            for k in range(0, len(partials)):
                signal += (1/partials[k]) * np.sin(k * omega * t)
                x = coefficients[k] * (4/np.pi)* signal
                env = ADSR.getadsr(x, envelope)
                x_env = x * env[:len(x)]
            sound.extend(x_env)
            
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

        return np.array(sound)

    def granular(self, s, grainSize, hopSize, timeScale, freqScale, timeVariation, pitchVariation):
        numGrains = int(len(s) / hopSize)
        s = np.pad(s, (0, grainSize), 'constant')

        grainOutputPositions = np.zeros(numGrains, dtype=np.uint64)
        grainOutputPitches = np.zeros(numGrains)
        
        for grainNum in range(numGrains):
            grainPosition = hopSize * grainNum
            grainOutputPosition = grainPosition / timeScale
            grainOutputPositions[grainNum] = grainOutputPosition
            grainOutputPitches[grainNum] = freqScale

        grainOutputPositions[1:] = grainOutputPositions[1:] + ((np.random.randn(numGrains - 1) * 2 - 1) * timeVariation)
        
        grainOutputPositions = grainOutputPositions.astype(np.uint64)
            
        grainOutputPitches = grainOutputPitches + ((np.random.randn(numGrains) * 2 - 1) * pitchVariation)

        minOutputPitch = np.min(grainOutputPitches)
        outputGrainSize = int(grainSize / minOutputPitch) + 1
        lastGrainOutputPosition = grainOutputPositions[-1]
        outputLength = int(lastGrainOutputPosition + outputGrainSize) + grainSize

        print(outputLength, outputGrainSize)
        output = np.zeros(outputLength)
        grainOutput = np.zeros(outputGrainSize)
        
        hanWin = np.hanning(grainSize)
        
        for grainNum in range(numGrains):
            grainOutput.fill(0)

            grainPosition = hopSize * grainNum
            grainOutputPosition = int(grainOutputPositions[grainNum])
            grainPitch = grainOutputPitches[grainNum]
            
            windowedGrain = hanWin * s[grainPosition:grainPosition + grainSize]
            windowedGrain = LinearWrap(windowedGrain)
            for grainOutputIdx in range(outputGrainSize):
                grainInputIdx = grainOutputIdx * grainPitch
                grainOutput[grainOutputIdx] = windowedGrain[grainInputIdx]
            print(grainOutputPosition, output[grainOutputPosition:grainOutputPosition+outputGrainSize].shape, grainOutput.shape)
            output[grainOutputPosition:grainOutputPosition+outputGrainSize] += grainOutput
        
        return output


