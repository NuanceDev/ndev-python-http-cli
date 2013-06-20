#!/usr/bin/python

import pyaudio
import wave
import sys

# Credit due: http://people.csail.mit.edu/hubert/pyaudio/

if len(sys.argv) < 2:
    print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
    sys.exit(-1)

def playback(outname):
    chunk_size = 1024
    paudio = pyaudio.PyAudio()
    file_to_play = wave.open(outname, 'rb')
    stream = paudio.open(format = paudio.get_format_from_width(file_to_play.getsampwidth()),
                         channels = file_to_play.getnchannels(),
                         rate = file_to_play.getframerate(),
                         output = True)
    data = file_to_play.readframes(chunk_size)
    while data != '':
         stream.write(data)
         data = file_to_play.readframes(chunk_size)
    stream.stop_stream()
    stream.close()
    paudio.terminate()

if __name__ == "__main__":
    playback('%s' % sys.argv[1])