#!/usr/bin/python

import sys, wave, pyaudio
from ndev.core import UserInput, cyan, red

# Credit due: http://people.csail.mit.edu/hubert/pyaudio/

def write_wav_file(outname, channels, samp_width, rate, data):
    wf = wave.open(outname, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(samp_width)
    wf.setframerate(rate)
    wf.writeframes(data)
    wf.close()

def record(outname):
    
    chunk = 1024
    format = pyaudio.paInt16
    channels = 1 if sys.platform == 'darwin' else 2
    record_cap = 10 # seconds

    p = pyaudio.PyAudio()

    devcount = p.get_device_count()
    
    print "Here are the available audio devices:"

    default_device_index = 0

    for device_index in range(devcount):
        device = p.get_device_info_by_index(device_index)
        print "[%s]  %s\tDefault Sample Rate: %i\t%s" % (device_index, device['name'], device['defaultSampleRate'], "Default" if device_index == default_device_index else "")

    user_input = UserInput(question="\nWhich device would you like to record audio from: ", input_type=int, default_value=default_device_index)
    desired_device_index = user_input.get_input()
	
    device = p.get_device_info_by_index(int(desired_device_index))

    try:
         print cyan("\nUsing device:\t%s" % device['name'])
         start = raw_input("\n[enter] to begin recording, [ctrl-c] to cancel\n")
    except KeyboardInterrupt:
         raise KeyboardInterrupt("\ncancelled recording")

    rate = int(device['defaultSampleRate'])
    stream = p.open(format=format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)
    print "o\t recording\t(ctrl+c to stop)"
    
    all = []
    try:
        for i in range(0, rate/chunk*record_cap):
            data = stream.read(chunk)
            all.append(data)
    except KeyboardInterrupt:
        pass
    finally:
        print "x\t done recording"
        stream.stop_stream()
        stream.close()
        p.terminate()
        write_wav_file(outname, channels, p.get_sample_size(format), rate, ''.join(all))
        return True

if __name__ == "__main__":
    
    if len(sys.argv) < 2:
        print("Records a wave file.\n\nUsage: %s output_filename.wav" % sys.argv[0])
        sys.exit(-1)
    
    file_name = '%s' % sys.argv[1]
    print "Recording to: %s\n" % file_name
    try:
        was_ok = record(file_name)
        if not was_ok:
            print "Failed"
    except KeyboardInterrupt as e:
        print red(e) 
        sys.exit(-1)
