#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from optparse import OptionParser
from ndev.core import NDEVCredentials, HEADER, red, green, yellow, UserInput
from ndev.tts import *

"""
CLI
"""
parser = OptionParser(usage="usage: %prog {destination_file_name.format} {text_to_synthesize} [options]")
parser.add_option("-l", "--lang", action="store", type="string", dest="language",
                  help="desired language via language code, i.e. en_US")
parser.add_option("-r", "--rate", action="store", type="int", dest="samplerate",
                  help="the sample rate to use for the create audio file if relevant, i.e. 16000")
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
    print yellow("\nUsing Language: %s (%s)\tVoice: %s\n" % (desired_tts_lang['display'], desired_tts_lang['properties']['code'], desired_tts_lang['properties']['voice']))
    
    try:

        filename = args[0]
        text = unicode(args[1],'utf-8')
        audio_type = TTS.get_audio_type(filename)

        sample_rate = None # doesn't have to be defined, depends on codec
        atype = TTS.Accept[audio_type]
        if 'rate' in atype:
            sample_rate = getattr(options, 'samplerate')
            if sample_rate != None and not sample_rate in atype['rate']:
                print red("%i is not an acceptable sample rate.\n" % sample_rate)
                sample_rate = None
            if sample_rate is None:
                num_rates = len(atype['rate'])
                if num_rates > 1:
                    print "The following sample rates are available for the '%s' format..\n" % audio_type
                    for index, rate in enumerate(atype['rate']):
                        print " [%i]  %sHz" % (index, rate)
                    sample_rate_index = UserInput(question="\nWhat sample rate would you like to use? ", input_type=int, default_value=0).get_input()
                    sample_rate = atype['rate'][sample_rate_index]
                else:
                    sample_rate = atype['rate'][0]
                print yellow("\nUsing Sample Rate: %s\n" % sample_rate)
        
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
