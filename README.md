# MUSI6202Synth
MUSI 6202 Spring 21 Final Project

Group 10: Nitin Hugar, Rishikesh Daoo and Sandeep Dasari

This repository is a basic implementation of an Additive and Granular Synth in Python.

### Usage 
```
python3 synth.py \
--input input/kiss.mid \
--samplerate 44100
--bitrate 32
inserts --reverb --flanger --vibrato --echo --filter
```

Paramter values for inserts and granular synth can be customized in runtime.

Example output:
```
python3 synth.py --input input/kiss.mid  inserts

Namespace(input='input/kiss.mid', samplerate=None, bitrate=None, chorus=False, flanger=False, vibrato=False, echo=False, reverb=False, filter=False)
Getting notes from Midi....
Enter space-seperated list of ADSR envelope values (0-1): 0.2 0.1 0.5 0.1
[0.2, 0.1, 0.5, 0.1]
Generating sound with Additive Synth....
Enter values of partials? (y/n): n
Adding default partials:  [1, 2, 3, 4]
Enter values of coefficients? (y/n): n
Adding default coefficients:  [1, 1, 1, 1]
Processing Inserts....
Granularize output? (y/n): n
Bypassing granular synth
Setting Sampling Rate to 48000
Setting Bitrate to 32
Writing output to output/output1.wav
(base) 2012s-MacBook-Pro:MUSI6202Synth a2012$ python3 synth.py --input input/kiss.mid  inserts
Namespace(input='input/kiss.mid', samplerate=None, bitrate=None, chorus=False, flanger=False, vibrato=False, echo=False, reverb=False, filter=False)
Getting notes from Midi....
Enter space-seperated list of ADSR envelope values (0-1): 0.2 0.1 0.4 0.2
[0.2, 0.1, 0.4, 0.2]
Generating sound with Additive Synth....
Enter values of partials? (y/n): n
Adding default partials:  [1, 2, 3, 4]
Enter values of coefficients? (y/n): n
Adding default coefficients:  [1, 1, 1, 1]
Processing Inserts....
Granularize output? (y/n): y
Enter custom values? (y/n): n
Setting Sampling Rate to 48000
Setting Bitrate to 32
Writing output to output/output1.wav
```

Note: Sum of ADR values in the envelope < 1.0

Outputs are written as .wav files to `\output`