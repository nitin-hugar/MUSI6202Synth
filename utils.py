import argparse
from music21 import *


def parse_arguments():
    parser = argparse.ArgumentParser(description="DSP Synth Implementation")

    subparsers = parser.add_subparsers(help='commands')

    # Additive:
    parser.add_argument('-i', '--input', type=str, metavar='', required=True, help='Input path of midi file')
    parser.add_argument('-w', '--wavetype', type=str, metavar='', required=True, help='Type of wave')

    # Granular:

    # ADSR:
    envelope = subparsers.add_parser('ADSR', help='Add ADSR envelope')
    envelope.add_argument('--envelope', nargs="+", type=float, help='Add ADSR Envolope')

    # Effects Group
    fx = subparsers.add_parser('effects', help='Add effects to the sound')
    # action=true stores false until the value is called
    fx.add_argument('-c', '--chorus', action='store_true', help='Add Chorus')
    fx.add_argument('-f', '--flanger', action='store_true', help='Add Flanger')
    fx.add_argument('-v', '--vibrato', action='store_true', help='Add Vibrato')
    fx.add_argument('-e', '--echo', action='store_true', help='Add Echo')
    fx.add_argument('-r', '--reverb', action='store_true', help='Add Reverb')

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
