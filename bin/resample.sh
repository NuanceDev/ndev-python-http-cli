#!/bin/bash

# usage: 
#	./downsample {file} {(optional)sample_rate:8000,11025,22050,44100}

file=$1
extension="${file##*.}"
filename="${file%.*}"
bit_rate=16

sample_rate=$2
if [ -z $sample_rate ]; then sample_rate="16k"; fi

out_file="${filename}_${sample_rate}.wav"

sox ${file} -b ${bit_rate} -r ${sample_rate} -c 1 ${out_file}

echo "${file} -> ${out_file}"
