# Synth interface for pre-processing CLI arguments, reading MIDI, ADSR and triggering Synth engines

from generators import Generators
import inserts
from utils import *
from postprocessing import *
from math import ceil

SAMPLING_RATE = 48000

if __name__ == '__main__':
    args = parse_arguments()
    print(args)

    # Get the input midi file and ADSR
    print("Getting notes from Midi....")
    path = args.input
    notes = Notes(path)
    val = input("Enter values for ADSR envelope? (y/n): ")
    if val == 'y':
        envelope = input("Enter space-seperated list of ADSR envelope values (0-1): ").split()
        adsr = list(map(float, envelope))
    elif val == 'n':
        adsr = [0.3, 0.2, 0.7, 0.2]

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
        sound = synth.additive(adsr, partials, coefficients)
    else:
        raise ValueError("Number of partials not equal to number of coefficeints")


    # Process Inserts Chain
    inserts = inserts.Inserts(sound, SAMPLING_RATE)
    print("Processing Inserts....")
    for key, value in vars(args).items():
        if key == 'chorus' and value is True:
            print('Chorus: ')
            val = input("Enter custom values? (y/n): ")
            if val == 'y':
                fmod = float(input("Frequency modulation (default:1.5): "))
                A = float(input("Amplitude (default:0.002): "))
                M = float(input("Number of delay samples (default:0.002): "))
                BL = float(input("Blend (default:1.0):"))
                FF = float(input("Feedforward (default:0.7):"))
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
                fmod = float(input("Frequency modulation (default:0.2):"))
                A = float(input("Amplitude (default:0.002):"))
                M = float(input("Number of delay samples (default:0.002):"))
                BL = float(input("Blend (default:0.7):"))
                FF = float(input("Feedforward (default:0.7):"))
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
                maxDelaySamps = int(input("Maximum Delay Samples (default:200):"))
                fmod = float(input("Frequency modulation (default:1.0):"))
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
                impulse_path = input("Enter path to impulse wav (default:UChurch.wav):")
                mix = float(input("Enter mix level (default:0.4):"))
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
                fmod = float(input("Frequency modulation (default:0.0):"))
                A = float(input("Amplitude (default:0.0):"))
                M = float(input("Number of delay samples (default:0.05):"))
                BL = float(input("Blend (default:0.7):"))
                FF = float(input("Feedforward (default:0.7):"))
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
                type = input("Filter type (default:lowpass):")
                gain = float(input("Gain (default:1.0):"))
                center_frequency = float(input("Center Frequency (default:2000):"))
                Q = float(input("Q Factor (default:0.8):"))
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
        custom_val = input("Enter custom values? (y/n): ")
        if custom_val == 'y':
            gs = int(input("Enter Grain Size (default:2048):"))
            hs = int(input("Enter Hop Size (default:128):"))
            ts = float(input("Enter Time Scale (default:1):"))
            fs = float(input("Enter Frequency Scale (default:1):"))
            tv = float(input("Enter Time Variation (default:15):"))
            fv = float(input("Enter Frequency Variation (default:0.0):"))
            sound = synth.granular(sound, gs, hs, ts, fs, tv, fv)
        elif custom_val == 'n':
            sound = synth.granular(sound)

    elif val == 'n':
        print('Bypassing granular synth')

    # Smoothing filter
    kernel_size = 10
    kernel = np.ones(kernel_size) / kernel_size
    sound = np.convolve(sound, kernel, mode='same')

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
