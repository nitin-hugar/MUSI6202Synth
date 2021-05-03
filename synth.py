# synth interface for pre-processing CLI arguments, reading MIDI, ADSR and triggering Synth engines

from music21 import *
from generators import Generators
import effects
import pyloudnorm as pyln
import matplotlib.pyplot as plt
import argparse
import soundfile as sf

SAMPLING_RATE = 48000


def parse_arguments():
    parser = argparse.ArgumentParser(description="DSP Synth Implementation")

    subparsers = parser.add_subparsers(help='commands')

    parser.add_argument('-i', '--input', type=str, metavar='', required=True, help='Input path of midi file')
    parser.add_argument('-w', '--wavetype', type=str, metavar='', required=True, help='Type of wave')

    # Effects Group
    fx = subparsers.add_parser('effects', help='Add effects to the sound')
    # action=true stores false until the value is called
    fx.add_argument('-c', '--chorus', action='store_true', help='Add Chorus')
    fx.add_argument('-f', '--flanger', action='store_true', help='Add Flanger')
    fx.add_argument('-v', '--vibrato', action='store_true', help='Add Vibrato')
    fx.add_argument('-e', '--echo', action='store_true', help='Add Echo')
    fx.add_argument('-r', '--reverb', action='store_true', help='Add Reverb')



    print(parser.parse_args())
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


if __name__ == '__main__':
    args = parse_arguments()

    # Get the imput midi file:
    print("Getting notes from Midi....")
    path = args.input
    notes = Notes(path)

    # Generate sound
    print("Generating sound....")
    numOfHarmonics = 20
    synth = Generators(notes, SAMPLING_RATE)
    sound = synth.make_sound(args.wavetype, numOfHarmonics)

    # set loudness to -12 LUFS
    print("Setting loudness to -12 LUFS....")
    meter = pyln.Meter(SAMPLING_RATE)
    loudness = meter.integrated_loudness(sound)
    sound = pyln.normalize.loudness(sound, loudness, -24.0)

    fx = effects.Effects(sound, SAMPLING_RATE)

    for key, value in vars(args).items():
        if key == 'chorus' and value is True:
            fx.chorus()
        elif key == 'flanger' and value is True:
            fx.flanger()
        elif key == 'vibrato' and value is True:
            fx.flanger()
        elif key == 'reverb' and value is True:
            fx.conv_reverb('impulses/UChurch.wav')

    sf.write('../output/output.wav', fx.data, SAMPLING_RATE)

    print("Done!!")
