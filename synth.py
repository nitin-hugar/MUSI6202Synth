# synth interface for pre-processing CLI arguments, reading MIDI, ADSR and triggering Synth engines

from generators import Generators
import effects
import pyloudnorm as pyln
import matplotlib.pyplot as plt
from utils import *
import soundfile as sf
from postprocessing import *
from math import ceil

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
    synth = Generators(notes, SAMPLING_RATE)
    partials = []
    coefficients = []
    for key, value in vars(args).items():
        if key == 'partials' and value is True:
            val = input("Enter values of partials? (y/n): ")
            if val == 'y':
                partials  = input("Enter a space-separated list of partials: ").split()
                partials = list(map(float, partials))
            elif val == 'n':
                partials=[1,2,3,4]
                print("Adding default partials: ",partials)
                
        elif key == 'coefficients' and value is True:
            val = input("Enter values of coefficients? (y/n): ")
            if val == 'y':
                coefficients  = input("Enter a space-separated list of partials: ").split()
                
                coefficients = list(map(float, coefficients))
            elif val == 'n':
                coefficients= [1] * len(partials)
                print("Adding default coefficients: ",coefficients)
    print(partials, coefficients)
    if (len(partials) == len(coefficients)):
        
        sound = synth.make_sound(args.envelope, partials, coefficients)
    else:
        raise ValueError("Number of partials not equal to number of coefficeints")


    # set loudness to -12 LUFS
    print("Setting loudness to -12 LUFS....")
    meter = pyln.Meter(SAMPLING_RATE)
    loudness = meter.integrated_loudness(sound)
    sound = pyln.normalize.loudness(sound, loudness, -24.0)

    fx = effects.Effects(sound, SAMPLING_RATE)
    print("Processing effects....")
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

    # Down sampling and Down quantization
    sound = np.asarray(fx.data, dtype=np.int32)
    sound = sound.astype(np.int32)
    # write(wave_file_path, fs, data)

    output = Downsampler()
    res = sound

    if args.samplerate is not None:
        output.output_fs = int(args.samplerate)

        down_factor = ceil(SAMPLING_RATE / float(output.output_fs))
        print(down_factor)
        t = len(sound) / SAMPLING_RATE
        down_sampled_data = output.down_sample(sound, down_factor, output.output_fs, SAMPLING_RATE)
        res = output.up_sample(down_sampled_data, int(SAMPLING_RATE / down_factor), output.output_fs, t)

    if args.bitrate is not None:
        output.output_br = int(args.bitrate)
        dq1 = output.down_quantization(res, 32, output.output_br)

    sf.write('output/output.wav', fx.data, SAMPLING_RATE)

    print("Done!!")
