#!/bin/bash

# relies on SOX to `play` the audio file

sample_rate="16k"
sample_filename="sample"

record_wav.py ${sample_filename}.wav \
&& resample.sh ${sample_filename}.wav ${sample_rate} \
&& asr_then_tts.py sample_${sample_rate}.wav \
&& play ${sample_filename}_${sample_rate}_tts.wav
