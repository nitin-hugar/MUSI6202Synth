# synth interface for pre-processing CLI arguments, reading MIDI, ADSR and triggering Synth engines

from generators import Generators
import effects
import pyloudnorm as pyln
import matplotlib.pyplot as plt
from utils import *
import soundfile as sf

SAMPLING_RATE = 48000


if __name__ == '__main__':
    args = parse_arguments()

    # Get the input midi file:
    print("Getting notes from Midi....")
    path = args.input
    notes = Notes(path)

    # Generate sound
    print("Generating sound....")
    numOfHarmonics = 20
    synth = Generators(notes, SAMPLING_RATE)
    sound = synth.make_sound(args.wavetype, args.envelope, numOfHarmonics)

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
