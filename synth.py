# synth interface for pre-processing CLI arguments, reading MIDI, ADSR and triggering Synth engines

from music21 import *
import soundfile as sf
from generators import Generators
import effects
import pyloudnorm as pyln


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

    print("Getting notes from Midi....")
    path = '../input/kiss.mid'
    notes = Notes(path)
    fs = 48000
    numOfHarmonics = 20

    print("Generating sound....")
    synth1 = Generators(notes, fs)
    sound = synth1.make_sound('square', numOfHarmonics)

    print("Setting loudness to -12 LUFS....")
    #set loudness to -12 LUFS
    meter = pyln.Meter(fs)
    loudness = meter.integrated_loudness(sound)
    sound = pyln.normalize.loudness(sound, loudness, -24.0)

    fx = effects.Effects(sound, fs)
    melody_chorus = fx.chorus(fmod=1.5)
    melody_flanger = fx.flanger()
    melody_vibrato = fx.vibrato()
    melody_echo = fx.echo()
    melody_reverb = fx.conv_reverb('impulses/Saieh_hallway.wav', 0.2)
    print("Writing out file....")
    sf.write('../output/melody_dry.wav', sound, fs)
    sf.write('../output/melody_chorus.wav', melody_chorus, fs)
    sf.write('../output/melody_flanger.wav', melody_flanger, fs)
    sf.write('../output/melody_vibrato.wav', melody_vibrato, fs)
    sf.write('../output/melody_echo.wav', melody_echo, fs)
    sf.write('../output/melody_reverb.wav', melody_reverb, fs)
    print("Done!!")

if __name__ == '__main__':
    main()
