#!/usr/bin/python
# -*- coding: utf-8 -*-

import json

"""
####################################################################################
# 
#  ##    ## ##     ##    ###    ##    ##  ######  ######## 
#  ###   ## ##     ##   ## ##   ###   ## ##    ## ##       
#  ####  ## ##     ##  ##   ##  ####  ## ##       ##       
#  ## ## ## ##     ## ##     ## ## ## ## ##       ######   
#  ##  #### ##     ## ######### ##  #### ##       ##       
#  ##   ### ##     ## ##     ## ##   ### ##    ## ##       
#  ##    ##  #######  ##     ## ##    ##  ######  ########
#
####################################################################################
"""

HEADER = """

NDEV HTTP Python CLI from Nuance Communications
    for more info see: http://nuancedev.github.io

"""

"""
UserInput validates against a particular data type.
It also checks the existence of the value.
If not present, or incorrectly entered, the default value is used.
	This is handled via a threshold of inputs. Currently 3.
"""
class UserInput(object):
	
	def __init__(self, question=None, input_type=str, default_value=None, threshold=3):
		self.question = question
		self.input_type = input_type
		self.default_value = default_value
		self.threshold = threshold
	
	def is_numeric_input(self, input):
		try:
			val = int(input)
			return True
		except ValueError:
			return False
		
	def get_input(self):
		times_asked = 0
		threshold = self.threshold
		while times_asked < threshold:
			user_input = self.get_user_input()
			if user_input != None:
				return user_input
			else:
				times_asked += 1
				if times_asked < threshold:
					num_left = threshold-times_asked
					suf = "s" if num_left is not 1 else ""
					print red("   Please supply an input of %s. %i more attempt%s before selecting default." % (str(self.input_type), num_left, suf))
		print yellow("   Using default value. Option [%s]" % self.default_value)
		return self.default_value
		
	def get_user_input(self):
		ret = raw_input(self.question).strip()
		is_ok = True
		if self.input_type == str:
			is_ok = ret != None and ret != ''
		elif self.input_type == int:
			is_ok = self.is_numeric_input(ret)
			if is_ok:
				ret = int(ret)
		return ret if is_ok else None

"""
These values are stored in a json file (see: NDEVCredentials.PATH).
Please check your email, or the ndev portal for the values you will want to provide in the json file.
"""
class NDEVCredentials(object):
	
	PATH = 'credentials.json'
	
	def __init__(self, credentials_path=None):
		self.app_id = None
		self.app_key = None
		self.asr_url = None
		self.asr_endpoint = None
		self.tts_url = None
		self.tts_endpoint = None
		self._load_credentials(credentials_path)
		
	def _load_credentials(self, credentials_path):
		p = credentials_path if credentials_path is not None else NDEVCredentials.PATH
		f = open(p, 'rb')
		j = json.loads(f.read())
		self.app_id = j['appId']
		self.app_key = j['appKey']
		self.asr_url = j['asrUrl']
		self.asr_endpoint = j['asrEndpoint']
		self.tts_url = j['ttsUrl']
		self.tts_endpoint = j['ttsEndpoint']
		f.close()
	
	def has_credentials(self):
		ret = self.app_id is not None
		ret &= self.app_key is not None
		ret &= len(self.app_id) > 0
		ret &= len(self.app_key) > 0
		return ret

"""
Base Response. Deals with parsing the HTML response that is returned from NDEV.
"""
class NDEVResponse(object):
	
	def __init__(self):
		self.parsed = False
		self.status_code = -1
		self.error_message = ""
		self.results = []
	
	def _parse_html_for_reason(self, text):
		start = text.index("<pre>")
		end = text.index("</pre>")
		if start > -1:
			start = start + len("<pre>")
		return text[start:end].strip()
		
	def _parse_response(self, response):
		if response is not None and response.text != '':
			if response.text.startswith("<html>"):
				self.error_message = "%s: %s" % (self.status_code, self._parse_html_for_reason(response.text))
			else:
				self.results = response.text.split("\n") # keep it in unicode
			self.parsed = True

	def was_successful(self):
		return self.parsed and self.status_code == 200

"""
Base Request
"""
class NDEVRequest(object):

	def __init__(self, credentials=None):
		self.app_id = credentials.app_id if credentials is not None else None
		self.app_key = credentials.app_key if credentials is not None else None
		self.requestor_id = u"fc2jvf7p" # Specifying this will create a voice profile. Use such that one ID per person.
		self.sample_rate = 16000
		self.nchannels = 1
		self.sample_width = 0

	def _build_header_value(self, o, t):
		hdr = o[t]
		ret = []
		for k in hdr.keys():
			v = hdr[k]
			if k != 'mimetype':
				if k == 'rate' and type(v) == list:
					if self.sample_rate not in v:
						raise Exception("Bad Sample Rate: %s is not supported" % self.sample_rate)
					v = v[v.index(self.sample_rate)]
				ret.append(k + '=' + str(v))
		value = "%s%s" % (hdr['mimetype'], '%s%s' % (';' if len(ret)>0 else '', ';'.join(ret)))
		return value

"""
Input method for languages
"""
def _get_language_input(type, data, default): # type = 'Recognition', 'Synthesis', o = ASR, TTS
	print "Select %s Language\n" % type
	i = 0 
	languages = list(data.Languages)
	languages.sort()
	for lang in languages:
		print " [%i]\t%-25s %s" % (i, lang, data.Languages[lang]['code'])
		i += 1
	selection = raw_input("\nWhich language (default: %s)? " % default)
	lang = languages[int(selection)] if len(selection) > 0 else None
	ret = {
		'display': lang,
		'properties': data.Languages[lang if lang is not None else default]
	}
	return ret
	
"""
Command Line Utilities
"""
def _color_func(code):
    def inner(text, bold=False):
        c = code
        if bold:
            c = "1;%s" % c
        return "\033[%sm%s\033[0m" % (c, text)
    return inner

red = _color_func('31')
green = _color_func('32')
yellow = _color_func('33')
blue = _color_func('34')
magenta = _color_func('35')
cyan = _color_func('36')
white = _color_func('37')
