# synth interface for pre-processing CLI arguments, reading MIDI, ADSR and triggering Synth engines

from music21 import *
import soundfile as sf
from generators import Generators
import effects


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


def main():
    # path = '../input/midi1.mid'
    # notes = Notes(path)
    # fs = 44100
    # numOfHarmonics = 40
    #
    # synth1 = Generators(notes, fs)
    # sound = synth1.make_sound('sine', numOfHarmonics)

    sound, fs = sf.read('../input/melody.wav')
    sound = sound[:, 0]

    fx = effects.Effects(sound, fs)
    melody_chorus = fx.chorus()
    melody_flanger = fx.flanger()
    melody_vibrato = fx.vibrato()
    melody_echo = fx.echo()
    melody_reverb = fx.conv_reverb('impulses/Cathey_learning_center.wav')

    sf.write('../output/melody_dry.wav', sound, fs)
    sf.write('../output/melody_chorus.wav', melody_chorus, fs)
    sf.write('../output/melody_flanger.wav', melody_flanger, fs)
    sf.write('../output/melody_vibrato.wav', melody_vibrato, fs)
    sf.write('../output/melody_echo.wav', melody_echo, fs)
    sf.write('../output/melody_reverb.wav', melody_reverb, fs)


if __name__ == '__main__':
    main()
