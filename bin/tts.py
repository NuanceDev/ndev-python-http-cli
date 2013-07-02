#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from optparse import OptionParser
from ndev.core import NDEVCredentials, HEADER, red, green, yellow
from ndev.tts import *

"""
CLI
"""
parser = OptionParser(usage="usage: %prog {destination_file.wav} {text_to_synthesize} [options]")
parser.add_option("-l", "--lang", action="store", type="string", dest="language",
                  help="desired language via language code")
(options, args) = parser.parse_args()

if __name__ == "__main__":

    """
    Validate
    """
    if len(args) != 2:
        parser.error("Please provide (i) a destination_file and (ii) the text to synthesize")
        sys.exit(-1)
    
    print green(HEADER)
    
    creds = NDEVCredentials()
    if not creds.has_credentials():
        print red("Please provide NDEV credentials.")
        sys.exit(-1)
    
    language = getattr(options, 'language')
    desired_tts_lang = TTS.get_language_input(language)
    print "\nUsing Language: %s (%s)\tVoice: %s\n" % (desired_tts_lang['display'], desired_tts_lang['properties']['code'], desired_tts_lang['properties']['voice'])

    filename = args[0]
    text = unicode(args[1],'utf-8')
    audio_type = TTS.get_audio_type(filename)

    sample_rate = None # doesn't have to be defined, depends on codec
    atype = TTS.Accept[audio_type]
    if 'rate' in atype:
         sample_rate = atype['rate'][0]
    
    try:
    
        synth_req = TTS.make_request(creds=creds,
                                    desired_tts_lang=desired_tts_lang,
                                    sample_rate=sample_rate,
                                    nchannels=1,
                                    sample_width=2,
                                    text=text,
                                    filename=filename,
                                    audio_type=audio_type)
    
        if synth_req.response.was_successful():
             print "\nText synthesized to file -> %s" % yellow(filename)
        else:
             print red("\nNDEV TTS Error %s" % synth_req.response.error_message)

    except Exception as e:
        print red(e)
        sys.exit(-1)
