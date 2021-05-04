# MUSI6202Synth
MUSI 6202 Spring 21 Final Project

Group 10: Nitin Hugar, Rishikesh Daoo and Sandeep Dasari

This repository is a basic implementation of an Additive and Granular Synth in Python.

### Usage 

python3 synth.py \
--input input/kiss.mid \
--envelope 0.2 0.5 0.8 0.1 \
--samplerate 44100
--bitrate 32
inserts --reverb --flanger --vibrato --echo --filter


Outputs are written as .wav files to `\output`