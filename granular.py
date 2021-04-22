# Granular Synth Engine
import numpy as np
from scipy.io import wavfile as wav

# def create_grain(filePath, grainSize):
#     fs,x = wav.read(filePath)
#     grainFrames = grainSize * fs
#
#     grains = []
#     start = 0
#     stop = 0 + grainFrames
#     while start < x.size - grainFrames:
#         if stop - start == grainFrames:
#             grains.append(x[start:stop])
#             start += grainFrames
#             stop += grainFrames
#
#         else:
#             x.append(np.zeros(stop-x.size))
#             grains.append(x[start:stop])
#             start += grainFrames
#             stop += grainFrames
#
#     return grains
#
# filePath = 'inputs/melody.wav'
# x = create_grain(filePath, 40e-3)
# print(x)



