# synth interface for pre-processing CLI arguments, reading MIDI, ADSR and triggering Synth engines

from generators import Generators
import effects
import filters
import pyloudnorm as pyln
import matplotlib.pyplot as plt
from utils import *
import soundfile as sf

SAMPLING_RATE = 48000

if __name__ == '__main__':
    args = parse_arguments()
    print(args)

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
    filt = filters.Filters(sound, SAMPLING_RATE)

    for key, value in vars(args).items():
        if key == 'chorus' and value is True:
            val = input("Enter Chorus parameter values? (y/n): ")
            if val == 'y':
                fmod = float(input("fmod: "))
                A = float(input("A: "))
                M = float(input("M: "))
                BL = float(input("BL: "))
                FF = float(input("FF: "))
                print("Adding Chorus...")
                fx.chorus(fmod, A, M, BL, FF)
                print('Chorus added')
            elif val == 'n':
                print("Adding Chorus...")
                fx.chorus()
                print('Chorus added')
            else:
                raise ValueError("Enter 'y' or 'n'")

        elif key == 'flanger' and value is True:
            val = input("Enter Flanger parameter values? (y/n): ")
            if val == 'y':
                fmod = float(input("fmod: "))
                A = float(input("A: "))
                M = float(input("M: "))
                BL = float(input("BL: "))
                FF = float(input("FF: "))
                print("Adding Flanger effect...")
                fx.flanger(fmod, A, M, BL, FF)
                print("Flanger added")
            elif val == 'n':
                print("Adding Flanger...")
                fx.flanger()
                print("Flanger added")
            else:
                raise ValueError("Enter 'y' or 'n'")

        elif key == 'vibrato' and value is True:
            val = input("Enter Vibrato parameter values? (y/n): ")
            if val == 'y':
                maxDelaySamps = int(input("Maximum Delay Samples: "))
                fmod = float(input("fmod: "))
                print("Adding Vibrato effect...")
                fx.vibrato(maxDelaySamps, fmod)
                print("Vibrato added")
            elif val == 'n':
                print("Adding Vibrato effect...")
                fx.vibrato()
                print("Vibrato added")
            else:
                raise ValueError("Enter 'y' or 'n'")

        elif key == 'reverb' and value is True:
            print("Reverb: ")
            val = input("Enter path to impulse file? (y/n): ")
            if val == 'y':
                impulse_path = input("Enter path to impulse wav: ")
                mix = float(input("Enter mix level (0-1): "))
                print("Adding Reverb...")
                fx.conv_reverb(impulse_path, mix)
                print("Reverb added")
            elif val == 'n':
                print("Adding Reverb...")
                fx.conv_reverb('impulses/UChurch.wav')
                print("Reverb added")
            else:
                raise ValueError("Enter 'y' or 'n'")

        elif key == 'echo' and value is True:
            val = input("Enter Echo parameter values? (y/n): ")
            if val == 'y':
                fmod = float(input("fmod: "))
                A = float(input("A: "))
                M = float(input("M: "))
                BL = float(input("BL: "))
                FF = float(input("FF: "))
                print("Adding Echo...")
                fx.chorus(fmod, A, M, BL, FF)
                print('Echo added')
            elif val == 'n':
                print("Adding Echo...")
                fx.chorus()
                print('Echo added')
            else:
                raise ValueError("Enter 'y' or 'n'")

        elif key == 'lowpass' and value is True:
            val = input("Enter lowpass filter parameters? (y/n): ")
            if val == 'y':
                Q = float(input("Q: "))
                center_freq = float(input("Center Frequency: "))
                gain = float(input("Gain: "))
                filt.biquad("lowpass", gain, center_freq, Q)
            elif val == 'n':
                print("Adding Lowpass filter...")
                filt.biquad(type="lowpass")
                print('Lowpass filter added')
            else:
                raise ValueError("Enter 'y' or 'n'")

        elif key == 'hipass' and value is True:
            val = input("Enter hipass filter parameters? (y/n): ")
            if val == 'y':
                Q = float(input("Q: "))
                center_freq = float(input("Center Frequency: "))
                gain = float(input("Gain: "))
                filt.biquad("hipass", gain, center_freq, Q)
            elif val == 'n':
                print("Adding Highpass filter...")
                filt.biquad(type="hipass")
                print('Hipass filter added')
            else:
                raise ValueError("Enter 'y' or 'n'")

        elif key == 'allpass' and value is True:
            val = input("Enter allpass filter parameters? (y/n): ")
            if val == 'y':
                Q = float(input("Q: "))
                center_freq = float(input("Center Frequency: "))
                gain = float(input("Gain: "))
                filt.biquad("allpass", gain, center_freq, Q)
            elif val == 'n':
                print("Adding Allpass filter...")
                filt.biquad(type="allpass")
                print('Allpass filter added')
            else:
                raise ValueError("Enter 'y' or 'n'")

        elif key == 'bandpass' and value is True:
            val = input("Enter bandpass filter parameters? (y/n): ")
            if val == 'y':
                Q = float(input("Q: "))
                center_freq = float(input("Center Frequency: "))
                gain = float(input("Gain: "))
                filt.biquad("bandpass", gain, center_freq, Q)
            elif val == 'n':
                print("Adding Bandpass filter...")
                filt.biquad(type="bandpass")
                print('Bandpass filter added')
            else:
                raise ValueError("Enter 'y' or 'n'")

        elif key == 'notch' and value is True:
            val = input("Enter notch filter parameters? (y/n): ")
            if val == 'y':
                Q = float(input("Q: "))
                center_freq = float(input("Center Frequency: "))
                gain = float(input("Gain: "))
                filt.biquad("notch", gain, center_freq, Q)
            elif val == 'n':
                print("Adding Notch filter...")
                filt.biquad(type="notch")
                print('Notch filter added')
            else:
                raise ValueError("Enter 'y' or 'n'")

        elif key == 'peak' and value is True:
            val = input("Enter peak filter parameters? (y/n): ")
            if val == 'y':
                Q = float(input("Q: "))
                center_freq = float(input("Center Frequency: "))
                gain = float(input("Gain: "))
                filt.biquad("peak", gain, center_freq, Q)
            elif val == 'n':
                print("Adding Peak filter...")
                filt.biquad(type="peak")
                print('Peak filter added')
            else:
                raise ValueError("Enter 'y' or 'n'")

        elif key == 'highshelf' and value is True:
            val = input("Enter high shelf filter parameters? (y/n): ")
            if val == 'y':
                Q = float(input("Q: "))
                center_freq = float(input("Center Frequency: "))
                gain = float(input("Gain: "))
                filt.biquad("highshelf", gain, center_freq, Q)
            elif val == 'n':
                print("Adding High shelf filter...")
                filt.biquad(type="highshelf")
                print('High shelf filter added')
            else:
                raise ValueError("Enter 'y' or 'n'")

        elif key == 'lowshelf' and value is True:
            val = input("Enter low shelf filter parameters? (y/n): ")
            if val == 'y':
                Q = float(input("Q: "))
                center_freq = float(input("Center Frequency: "))
                gain = float(input("Gain: "))
                filt.biquad("lowshelf", gain, center_freq, Q)
            elif val == 'n':
                print("Adding Low shelf filter...")
                filt.biquad(type="lowshelf")
                print('Low shelf filter added')
            else:
                raise ValueError("Enter 'y' or 'n'")

    sf.write('output/output.wav', filt.data, SAMPLING_RATE)

    print("Done!!")
