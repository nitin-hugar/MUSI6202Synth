# Synth interface for pre-processing CLI arguments, reading MIDI, ADSR and triggering Synth engines

from generators import Generators
import inserts
import filters
import pyloudnorm as pyln
import matplotlib.pyplot as plt
from utils import *
from postprocessing import *
from math import ceil
import soundfile as sf

SAMPLING_RATE = 48000

if __name__ == '__main__':
    args = parse_arguments()
    print(args)

    # Get the input midi file:
    print("Getting notes from Midi....")
    path = args.input
    notes = Notes(path)

    # Generate sound with Additive synth
    print("Generating sound with Additive Synth....")
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
    inserts = inserts.Inserts(sound, SAMPLING_RATE)
    print("Processing Inserts....")
    for key, value in vars(args).items():
        if key == 'chorus' and value is True:
            print('Chorus :')
            val = input("Enter custom values? (y/n): ")
            if val == 'y':
                fmod = float(input("Frequency modulation: "))
                A = float(input("Amplitude: "))
                M = float(input("Number of samples (delay): "))
                BL = float(input("Blend: "))
                FF = float(input("Feedforward: "))
                print("Adding Chorus...")
                inserts.chorus(fmod, A, M, BL, FF)
                print('Chorus added')
            elif val == 'n':
                print("Adding Chorus with default values...")
                inserts.chorus()
                print('Chorus added')
            else:
                raise ValueError("Enter 'y' or 'n'")

        elif key == 'flanger' and value is True:
            print('Flanger :')
            val = input("Enter custom values? (y/n): ")
            if val == 'y':
                fmod = float(input("Frequency modulation: "))
                A = float(input("Amplitude: "))
                M = float(input("Number of samples (delay): "))
                BL = float(input("Blend: "))
                FF = float(input("Feedforward: "))
                print("Adding Flanger effect...")
                inserts.flanger(fmod, A, M, BL, FF)
                print("Flanger added")
            elif val == 'n':
                print("Adding Flanger with default values...")
                inserts.flanger()
                print("Flanger added")
            else:
                raise ValueError("Enter 'y' or 'n'")

        elif key == 'vibrato' and value is True:
            print('Vibrato :')
            val = input("Enter custom values? (y/n): ")
            if val == 'y':
                maxDelaySamps = int(input("Maximum Delay Samples: "))
                fmod = float(input("Frequency modulation: "))
                print("Adding Vibrato effect with default values...")
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
                print("Adding Reverb with default values...")
                inserts.conv_reverb('impulses/UChurch.wav')
                print("Reverb added")
            else:
                raise ValueError("Enter 'y' or 'n'")

        elif key == 'echo' and value is True:
            print("Echo: ")
            val = input("Enter custom values? (y/n): ")
            if val == 'y':
                fmod = float(input("Frequency modulation: "))
                A = float(input("Amplitude: "))
                M = float(input("Number of samples (delay): "))
                BL = float(input("Blend: "))
                FF = float(input("Feedforward: "))
                print("Adding Echo...")
                inserts.chorus(fmod, A, M, BL, FF)
                print('Echo added')
            elif val == 'n':
                print("Adding Echo with default values...")
                inserts.chorus()
                print('Echo added')
            else:
                raise ValueError("Enter 'y' or 'n'")

        elif key == 'filter' and value is True:
            print("Filter: ")
            val = input("Enter custom values? (y/n): ")
            if val == 'y':
                print("Types: lowpass, hipass, bandpass, allpass, notch, peak, hishelf, lowshelf")
                type = input("Filter type: ")
                gain = float(input("Gain (0-1): "))
                center_frequency = float(input("Center Frequency: "))
                Q = float(input("Q Factor (0-1): "))
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

    # Normalize Audio
    flag = max(sound) if max(sound) else 1
    x = np.divide(sound, flag)
    x = x * np.iinfo(np.int32).max
    x = x.astype(np.int32)

    data = np.asarray(x, dtype=np.int32)
    sampling = Downsampler()
    output = data

    # Downsampling 
    if args.samplerate is not None:
        print("Setting Sampling Rate to %s...." % args.samplerate)
        sampling.output_fs = int(args.samplerate)
        down_factor = ceil(SAMPLING_RATE / float(sampling.output_fs))
        t = len(output) / SAMPLING_RATE
        down_sampled_data = sampling.down_sample(output, down_factor, sampling.output_fs, SAMPLING_RATE)
        output = sampling.up_sample(down_sampled_data, int(SAMPLING_RATE / down_factor), sampling.output_fs, t)
    else:
        print("Setting Sampling Rate to 48000")

    # Quantization
    if args.bitrate is not None:
        print("Setting Bitrate to %s...." % args.bitrate)
        sampling.output_br = int(args.bitrate)
        output = sampling.down_quantization(output, 32, sampling.output_br)
    else:
        print("Setting Bitrate to 32")

    output_path = 'output/output1.wav'
    print("Writing output to %s" % output_path)
    sampling.write_wav(output_path, output, sampling.output_fs, sampling.output_br)
