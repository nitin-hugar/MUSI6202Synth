# synth interface for pre-processing CLI arguments, reading MIDI, ADSR and triggering Synth engines

from generators import Generators
import effects
import filters
import pyloudnorm as pyln
import matplotlib.pyplot as plt
from utils import *
from postprocessing import *
from math import ceil
import soundfile as sf

SAMPLING_RATE = 48000

if __name__ == '__main__':
    args = parse_additive_arguments()
    print(args)

    # Get the input midi file:
    print("Getting notes from Midi....")
    path = args.input
    notes = Notes(path)

    # Generate sound with Additive synth
    print("Generating sound....")
    synth = Generators(notes, SAMPLING_RATE)

    val = input("Enter values of partials? (y/n): ")
    if val == 'y':
        partials  = input("Enter a space-separated list of partials: ").split()
        partials = list(map(float, partials))
    elif val == 'n':
        partials=[1,2,3,4]
        print("Adding default partials: ",partials)

    val = input("Enter values of coefficients? (y/n): ")            
    if val == 'y':
        coefficients  = input("Enter a space-separated list of coefficients: ").split()        
        coefficients = list(map(float, coefficients))
    elif val == 'n':
        coefficients= [1] * len(partials)
        print("Adding default coefficients: ",coefficients)

    partials = [1, 2, 3, 4]
    coefficients = [1] * len(partials)

    if len(partials) == len(coefficients):
        sound = synth.additive(args.envelope, partials, coefficients)
    else:
        raise ValueError("Number of partials not equal to number of coefficeints")

    # Process Inserts Chain
    inserts = effects.Effects(sound, SAMPLING_RATE)
    print("Processing Inserts....")
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
                inserts.chorus(fmod, A, M, BL, FF)
                print('Chorus added')
            elif val == 'n':
                print("Adding Chorus...")
                inserts.chorus()
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
                inserts.flanger(fmod, A, M, BL, FF)
                print("Flanger added")
            elif val == 'n':
                print("Adding Flanger...")
                inserts.flanger()
                print("Flanger added")
            else:
                raise ValueError("Enter 'y' or 'n'")

        elif key == 'vibrato' and value is True:
            val = input("Enter Vibrato parameter values? (y/n): ")
            if val == 'y':
                maxDelaySamps = int(input("Maximum Delay Samples: "))
                fmod = float(input("fmod: "))
                print("Adding Vibrato effect...")
                inserts.vibrato(maxDelaySamps, fmod)
                print("Vibrato added")
            elif val == 'n':
                print("Adding Vibrato effect...")
                inserts.vibrato()
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
                inserts.conv_reverb(impulse_path, mix)
                print("Reverb added")
            elif val == 'n':
                print("Adding Reverb...")
                inserts.conv_reverb('impulses/UChurch.wav')
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
                inserts.chorus(fmod, A, M, BL, FF)
                print('Echo added')
            elif val == 'n':
                print("Adding Echo...")
                inserts.chorus()
                print('Echo added')
            else:
                raise ValueError("Enter 'y' or 'n'")

        elif key == 'filter' and value is True:
            val = input("Enter Filter parameter values? (y/n): ")
            if val == 'y':
                print("Types: lowpass, hipass, bandpass, allpass, notch, peak, hishelf, lowshelf")
                type = input("Filter type: ")
                gain = float(input("Gain(0-1): "))
                center_frequency = float(input("Center Frequency: "))
                Q = float(input("Q Factor(0-1): "))
                print("Adding filter....")
                inserts.filters(type, gain, center_frequency, Q)
                print("Filtering added")

            elif val == 'n':
                print("Adding Filter with default values...")
                inserts.filters()
                print('Filtering added')
            else:
                raise ValueError("Enter 'y' or 'n'")

sound = inserts.data

# Granularization
val = input("Granularize output? (y/n): ")
if val == 'y':
    gs = int(input("Enter Grain Size: "))
    hs = int(input("Enter Hop Size: "))
    ts = float(input("Enter Time Scale: "))
    fs = float(input("Enter Frequency Scale: "))
    tv = float(input("Enter Time Variation: "))
    fv = float(input("Enter Frequency Variation: "))
    sound = synth.granular(sound, gs, hs, ts, fs, tv, fv)

elif val == 'n':
    print('Bypassing granular synth')

# Normalize Audio:
flag = max(sound) if max(sound) else 1
x = np.divide(sound, flag)
x = x * np.iinfo(np.int32).max
x = x.astype(np.int32)

data = np.asarray(x, dtype=np.int32)
sampling = Downsampler()
output = data

print("Setting Sampling Rate to %s...." % args.samplerate)
if args.samplerate is not None:
    sampling.output_fs = int(args.samplerate)

    down_factor = ceil(SAMPLING_RATE / float(sampling.output_fs))
    t = len(output) / SAMPLING_RATE
    down_sampled_data = sampling.down_sample(output, down_factor, sampling.output_fs, SAMPLING_RATE)
    output = sampling.up_sample(down_sampled_data, int(SAMPLING_RATE / down_factor), sampling.output_fs, t)

print("Setting Bitrate to %s...." % args.bitrate)
if args.bitrate is not None:
    sampling.output_br = int(args.bitrate)
    output = sampling.down_quantization(output, 32, sampling.output_br)

output_path = 'output/output1.wav'
print("Writing output to %s" % output_path)
sampling.write_wav(output_path, output, sampling.output_fs, sampling.output_br)
