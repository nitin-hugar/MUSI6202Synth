# synth interface for pre-processing CLI arguments, reading MIDI, ADSR and triggering Synth engines

from generators import Generators
import effects
from utils import *
from postprocessing import *
from math import ceil
import soundfile as sf
import pyloudnorm as pyln


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

    partials = [1, 2, 3, 4]
    coefficients = [1] * len(partials)

    if len(partials) == len(coefficients):
        sound = synth.make_sound(args.envelope, partials, coefficients)
    else:
        raise ValueError("Number of partials not equal to number of coefficeints")

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

#Normalize Audio:
sound = fx.data
flag = max(sound) if max(sound) else 1
x =  np.divide(sound, flag)
x = x * np.iinfo(np.int32).max
x = x.astype(np.int32)

data = np.asarray(x, dtype=np.int32)
sampling = Downsampler()
output = data

print("Setting Sampling Rate to %s...." %args.samplerate)
if args.samplerate is not None:
    sampling.output_fs = int(args.samplerate)

    down_factor = ceil(SAMPLING_RATE / float(sampling.output_fs))
    t = len(output) / SAMPLING_RATE
    down_sampled_data = sampling.down_sample(output, down_factor, sampling.output_fs, SAMPLING_RATE)
    output = sampling.up_sample(down_sampled_data, int(SAMPLING_RATE / down_factor), sampling.output_fs, t)

print("Setting Bitrate to %s...." %args.bitrate)
if args.bitrate is not None:
    sampling.output_br = int(args.bitrate)
    output = sampling.down_quantization(output, 32, sampling.output_br)

output_path = '../output/output1.wav'
print("Writing output to %s" %output_path)
sampling.write_wav(output_path, output, sampling.output_fs, sampling.output_br)
