#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys, time
from optparse import OptionParser
from ndev.core import red,green,cyan,yellow,magenta,NDEVCredentials,HEADER
from ndev.asr import *
from ndev.tts import *

"""
CLI
"""
parser = OptionParser(usage="usage: %prog {source_file.wav} [options]")
parser.add_option("-l", "--lang", action="store", type="string", dest="language",
                  help="desired language via language code")
parser.add_option("-v", "--verbose", action="store_true", dest="verbose",
                  help="specify whether or not you want to see the raw HTTP output")
(options, args) = parser.parse_args()

"""
Takes a file, sends chunks to ASR servlet, then passes reco results through to TTS servlet 
"""
if __name__ == "__main__":
    
    if len(args) != 1:
        parser.error("must provide a source_file to perform recognition on")
        sys.exit(-1)
    
    """
    Settings
    """
    wants_verbose_logging = getattr(options,'verbose')

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
    
    start_time = time.time()
    
    creds = NDEVCredentials()
    if not creds.has_credentials():
        print red("No NDEV Credentials. Please update %s" % NDEVCredentials.PATH)
        sys.exit(-1)
    
    filename = args[0]
    language = getattr(options,'language')
    desired_asr_lang = ASR.get_language_input(language)
    print "\nOK. Using language: %s (%s)\n" % (desired_asr_lang['display'], desired_asr_lang['properties']['code'])
    
    """
    ASR
    """
    try:
        
        asr_req = ASR.make_request(creds=creds, desired_asr_lang=desired_asr_lang, filename=filename)
    
        if asr_req.response.was_successful():
        
            print "\nNDEV ASR determined the audio file %s to be saying\n\n  %s\n" % (yellow(filename), magenta(asr_req.response.get_recognition_result()))
        
            """
            TTS
            """
        
            print "NDEV TTS being applied to recognition."
            desired_tts_lang = TTS.get_language_input(desired_asr_lang['properties']['code'])
            print "\nUsing Language: %s (%s)\tVoice: %s\n" % (desired_tts_lang['display'], desired_tts_lang['properties']['code'], desired_tts_lang['properties']['voice'])
        
            fname = '%s_tts.wav' % filename[0:filename.rindex('.')]
        
            default_audio_type = 'wav'
            synth_req = TTS.make_request(creds=creds,
                                        desired_tts_lang=desired_tts_lang,
                                        sample_rate=asr_req.sample_rate,
                                        nchannels=asr_req.nchannels,
                                        sample_width=asr_req.sample_width,
                                        text=asr_req.response.get_recognition_result(), # unicode
                                        filename=fname,
                                        audio_type=default_audio_type) # uses wav as default output 
        
            if synth_req.response.was_successful():
                print "\nNDEV synthesized text to file %s (%s bytes)" % (yellow(fname), yellow(os.path.getsize(fname)))
            else:
                print "NDEV TTS Error %s" % synth_req.response.error_message
                sys.exit(-1)
                
        else:
            print "\nNDEV ASR Error %s" % asr_req.response.error_message
            sys.exit(-1)

        print cyan("\nTook:\t%fs" % (time.time() - start_time))

    except Exception as e:
        print red(e)
        sys.exit(-1)