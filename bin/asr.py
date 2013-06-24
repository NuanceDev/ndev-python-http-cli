#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys
from optparse import OptionParser
from ndev.core import NDEVCredentials, HEADER, red, magenta
from ndev.asr import *

"""
CLI
"""
parser = OptionParser(usage="usage: %prog {source_file.wav} [options]")
parser.add_option("-l", "--lang", action="store", type="string", dest="language",
                  help="desired language via language code")
(options, args) = parser.parse_args()

"""
Validate
"""

if __name__ == "__main__":
    
    if len(args) != 1:
        parser.error("Please provide a source_file to perform recognition on.")
        sys.exit(-1)

    print green(HEADER)
    
    creds = NDEVCredentials()
    if not creds.has_credentials():
         print red("Please provide NDEV credentials.")
         sys.exit(-1)

    filename = args[0]
    
    language = getattr(options, 'language')
    desired_asr_lang = ASR.get_language_input(language)
    print "OK. Using Language: %s (%s)\n" % (desired_asr_lang['display'], desired_asr_lang['properties']['code'])

    try:
        asr_req = ASR.make_request(creds=creds, desired_asr_lang=desired_asr_lang, filename=filename)

        if asr_req.response.was_successful():
             print "\n%s" % magenta(asr_req.response.get_recognition_result()) # instead of looping through, pick head
        else:
             print "\n%s" % red(asr_req.response.error_message)
    except Exception as e:
        print red(e)
        sys.exit(-1)
