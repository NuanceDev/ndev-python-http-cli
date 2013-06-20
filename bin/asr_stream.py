#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
brew install libsamplerate
pip install scikits.samplerate
"""

import os, sys, pyaudio, numpy
from sys import stdout
from optparse import OptionParser
from ndev.core import NDEVCredentials, HEADER, red, green, magenta
from ndev.asr import ASR, ChunkedASRRequest
from scikits.samplerate import resample


"""
CLI
"""
parser = OptionParser(usage="usage: %prog [options]")
parser.add_option("-l", "--lang", action="store", type="string", dest="language",
                  help="desired language via language code")
parser.add_option("-s", "--samplerate", action="store", type="int", dest="samplerate",
                  help="specify the desired samplerate to use for audio xfer", default=16000)
parser.add_option("-v", "--verbose", action="store_true", dest="verbose",
                  help="specify whether or not you want to see the raw HTTP output")
(options, args) = parser.parse_args()

"""
generator file for streaming the audio file in chunks
"""
def __stream_audio_realtime(filepath, rate=44100):
    total_chunks = 0
    format = pyaudio.paInt16
    channels = 1 if sys.platform == 'darwin' else 2
    record_cap = 10 # seconds
    p = pyaudio.PyAudio()
    stream = p.open(format=format, channels=channels, rate=rate, input=True, frames_per_buffer=ASR.chunk_size)
    print "o\t recording\t\t(Ctrl+C to stop)"
    try:
        desired_rate = float(desired_sample_rate) / rate # desired_sample_rate is an INT. convert to FLOAT for division.
        for i in range(0, rate/ASR.chunk_size*record_cap):
            data = stream.read(ASR.chunk_size)
            _raw_data = numpy.fromstring(data, dtype=numpy.int16)
            _resampled_data = resample(_raw_data, desired_rate, "sinc_best").astype(numpy.int16).tostring()
            total_chunks += len(_resampled_data)
            stdout.write("\r  bytes sent: \t%d" % total_chunks)
            stdout.flush()
            yield _resampled_data
        stdout.write("\n\n")
    except KeyboardInterrupt:
        pass
    finally:
        print "x\t done recording"
        stream.stop_stream()
        stream.close()
        p.terminate()   
        # TODO: write wav file here for trail/debugging purposes

"""
This method will stream real time audio while performing a chunked ASR request to NDEV.
"""
def stream_asr(creds=None, desired_asr_lang=None, desired_sample_rate=16000):
    
    if creds is None:
        raise "Need credentials."
        
    if desired_asr_lang is None:
        raise "Please provide a language."

    aReq = ChunkedASRRequest(desired_asr_lang, credentials=creds)
    aReq.sample_width = 2 # unnecessary?
    aReq.sample_rate = desired_sample_rate
    result = aReq.analyze(__stream_audio_realtime)

    if result.was_successful():
        print green("✓ ASR",bold=True)
    else:
        print red("× ASR",bold=True)

    return aReq

"""
"""
if __name__ == "__main__":

    """
    Settings
    """
    wants_verbose_logging = getattr(options,'verbose')
    desired_sample_rate = getattr(options,'samplerate')

    if wants_verbose_logging:
        import logging
        import httplib
        httplib.HTTPConnection.debuglevel = 1
        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True

    print green(HEADER)

    creds = NDEVCredentials()
    if not creds.has_credentials():
        print red("Please provide NDEV credentials.")
        sys.exit(-1)
    
    language = getattr(options, 'language')
    desired_asr_lang = ASR.get_language_input(language)
    print "\nOK. Going forward, will use %s (%s) as the language.\n" % (desired_asr_lang['display'], desired_asr_lang['properties']['code'])

    asr_req = stream_asr(creds=creds, desired_asr_lang=desired_asr_lang, desired_sample_rate=desired_sample_rate)
    
    if asr_req.response.was_successful():
        print "\nNDEV ASR determined \n\n  %s\n" %  magenta(asr_req.response.get_recognition_result())
    else:
        print "\nNDEV ASR failed %s" % asr_req.response.error_message
