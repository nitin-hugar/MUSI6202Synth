import argparse
import numpy as np
import math
from music21 import *


def parse_arguments():
    synth_parser = argparse.ArgumentParser(description="Synth type parser")
    synth_subparser = synth_parser.add_subparsers(help='commands')

    # Additive:
    synth_subparser.add_argument('-i', '--input', type=str, metavar='', required=True, help='Input path of midi file')
    synth_subparser.add_argument('-w', '--wavetype', type=str, metavar='', required=True, help='Type of wave')
    synth_subparser.add_argument('--envelope', nargs=4, type=float, metavar='', required=True, help='Add ADSR Envelope')
    # Granular:

    fx_parser = argparse.ArgumentParser()
    # Effects Group
    fx = fx_parser.add_parser('effects', help='Add effects to the sound')
    # action=true stores false until the value is called
    fx_parser.add_argument('-c', '--chorus',action='store_true', help='Add Chorus')
    fx_parser.add_argument('-f', '--flanger', action='store_true', help='Add Flanger')
    fx_parser.add_argument('-v', '--vibrato', action='store_true', help='Add Vibrato')
    fx_parser.add_argument('-e', '--echo', action='store_true', help='Add Echo')
    fx_parser.add_argument('-r', '--reverb', action='store_true', help='Add Reverb')

    #Filters Group
    filt_parser = argparse.ArgumentParser()

    filt_subparser = filt_parser.add_parser('filters', help='Add filter to the sound')

    filt_subparser.add_argument('-lp', '--lowpass', action='store_true', help='Add lowpass filter')
    filt_subparser.add_argument('-hp', '--hipass', action='store_true', help='Add hipass filter')
    filt_subparser.add_argument('-bp', '--bandpass', action='store_true', help='Add hipass filter')
    filt_subparser.add_argument('-ap', '--allpass', action='store_true', help='Add hipass filter')
    filt_subparser.add_argument('-pk', '--peak', action='store_true', help='Add hipass filter')
    filt_subparser.add_argument('-nt', '--notch', action='store_true', help='Add hipass filter')
    filt_subparser.add_argument('-hs', '--highshelf', action='store_true', help='Add hipass filter')
    filt_subparser.add_argument('-ls', '--lowshelf', action='store_true', help='Add hipass filter')

    return parser.parse_args()


class Notes:
    def __init__(self, inputPath):
        self.inputPath = inputPath
        self.notenames, self.durations, self.frequencies = self.parseMidi()

    def parseMidi(self):
        midiData = converter.parse(self.inputPath)
        notes = midiData.flat.notesAndRests
        notenames = []
        durations = []
        frequencies = []
        for i in notes:
            if i.isNote:
                notenames.append(i.pitch.nameWithOctave)
                durations.append(i.quarterLength)
                frequencies.append(i.pitch.frequency)
            else:
                notenames.append(0)
                durations.append(i.quarterLength)
                frequencies.append(0)

        return notenames, durations, frequencies

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
