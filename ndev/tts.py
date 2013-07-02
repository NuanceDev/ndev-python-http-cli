#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys, wave, requests, time
from core import NDEVRequest, NDEVResponse, _get_language_input, red, green

"""
Constants as per the NDEV HTTP spec for TTS
"""

class TTS(object):
	
	ContentType = {
		'text': 'text/plain; charset=utf-8',
		'uri': 'message/external-body'
	}
	
	Accept = {
		'mp3': {
			'mimetype': 'audio/mpeg' # bit rate: 128kbps
		},
		'wav': {
			'mimetype': 'audio/x-wav',
			'codec': 'pcm',
			'bit': 16,
			'rate': [8000,16000,22000]
		},
		'speex': {
			'mimetype': 'audio/x-speex',
			'rate': [8000,16000]
		},
		'amr': {
			'mimetype': 'audio/amr'
		}
	}
	
	Languages = {
	  "Arabic": {
	    "code": "ar_WW",
	    "voice": [
	      "Maged"
	    ],
	    "gender": [
	      "M"
	    ]
	  },
	  "Australian English": {
	    "code": "en_AU",
	    "voice": [
	      "Karen",
	      "Lee"
	    ],
	    "gender": [
	      "F",
	      "M"
	    ]
	  },
	  "US English": {
	    "code": "en_US",
	    "voice": [
	      "Allison",
	      "Carol",
	      "Samantha",
	      "Tom"
	    ],
	    "gender": [
	      "F",
	      "F",
	      "F",
	      "M"
	    ]
	  },
	  "UK English": {
	    "code": "en_UK",
	    "voice": [
	      "Serena",
	      "Daniel"
	    ],
	    "gender": [
	      "F",
	      "M"
	    ]
	  },
	  "Bahasa (Indonesia)": {
	    "code": "id_ID",
	    "voice": [
	      "Damayanti"
	    ],
	    "gender": [
	      "F"
	    ]
	  },
	  "Basque": {
	    "code": "eu_ES",
	    "voice": [
	      "Arantxa"
	    ],
	    "gender": [
	      "F"
	    ]
	  },
	  "Belgian Dutch": {
	    "code": "nl_BE",
	    "voice": [
	      "Ellen",
	      "Ellen"
	    ],
	    "gender": [
	      "F",
	      "F"
	    ]
	  },
	  "Cantonese": {
	    "code": "zh_HK",
	    "voice": [
	      "Sin-Ji"
	    ],
	    "gender": [
	      "F"
	    ]
	  },
	  "Catalan": {
	    "code": "ca_ES",
	    "voice": [
	      "Nuria"
	    ],
	    "gender": [
	      "F"
	    ]
	  },
	  "Czech": {
	    "code": "cs_CZ",
	    "voice": [
	      "Zuzana"
	    ],
	    "gender": [
	      "F"
	    ]
	  },
	  "Danish": {
	    "code": "da_DK",
	    "voice": [
	      "Ida"
	    ],
	    "gender": [
	      "F"
	    ]
	  },
	  "Dutch": {
	    "code": "nl_NL",
	    "voice": [
	      "Xander",
	      "Claire"
	    ],
	    "gender": [
	      "M",
	      "F"
	    ]
	  },
	  "Finnish": {
	    "code": "fi_FI",
	    "voice": [
	      "Mikko"
	    ],
	    "gender": [
	      "F"
	    ]
	  },
	  "French": {
	    "code": "fr_FR",
	    "voice": [
	      "Audrey-ML*",
	      "Virginie",
	      "Sebastien",
	      "Thomas"
	    ],
	    "gender": [
	      "F",
	      "F",
	      "M",
	      "M"
	    ]
	  },
	  "Canadian French": {
	    "code": "fr_CA",
	    "voice": [
	      "Julie",
	      "Felix"
	    ],
	    "gender": [
	      "F",
	      "M"
	    ]
	  },
	  "German": {
	    "code": "de_DE",
	    "voice": [
	      "Anna",
	      "Steffi",
	      "Yannick"
	    ],
	    "gender": [
	      "F",
	      "F",
	      "M"
	    ]
	  },
	  "Greek": {
	    "code": "el_GR",
	    "voice": [
	      "Alexandros",
	      "Melina"
	    ],
	    "gender": [
	      "M",
	      "F"
	    ]
	  },
	  "Hindi": {
	    "code": "hi_IN",
	    "voice": [
	      "Lekha"
	    ],
	    "gender": [
	      "F"
	    ]
	  },
	  "Hungarian": {
	    "code": "hu_HU",
	    "voice": [
	      "Eszter"
	    ],
	    "gender": [
	      "F"
	    ]
	  },
	  "Indian English": {
	    "code": "en_IN",
	    "voice": [
	      "Sangeeta"
	    ],
	    "gender": [
	      "F"
	    ]
	  },
	  "Irish English": {
	    "code": "en_IE",
	    "voice": [
	      "Moira"
	    ],
	    "gender": [
	      "F"
	    ]
	  },
	  "Italian": {
	    "code": "it_IT",
	    "voice": [
	      "Alice-ML*",
	      "Silvia",
	      "Paolo"
	    ],
	    "gender": [
	      "F",
	      "F",
	      "M"
	    ]
	  },
	  "Japanese": {
	    "code": "jp_JP",
	    "voice": [
	      "Kyoko"
	    ],
	    "gender": [
	      "F"
	    ]
	  },
	  "Korean": {
	    "code": "ko_KR",
	    "voice": [
	      "Narae"
	    ],
	    "gender": [
	      "F"
	    ]
	  },
	  "Mandarin": {
	    "code": "zh_CN",
	    "voice": [
	      "Tian-Tian",
	      "Ting-Ting"
	    ],
	    "gender": [
	      "F",
	      "F"
	    ]
	  },
	  "Taiwanese Mandarin": {
	    "code": "zh_TW",
	    "voice": [
	      "Mei-Jia",
	      "Ya-Ling"
	    ],
	    "gender": [
	      "F",
	      "F"
	    ]
	  },
	  "Norwegian": {
	    "code": "no_NO",
	    "voice": [
	      "Stine"
	    ],
	    "gender": [
	      "F"
	    ]
	  },
	  "Polish": {
	    "code": "pl_PL",
	    "voice": [
	      "Agata"
	    ],
	    "gender": [
	      "F"
	    ]
	  },
	  "Portuguese": {
	    "code": "pt_PT",
	    "voice": [
	      "Joana"
	    ],
	    "gender": [
	      "F"
	    ]
	  },
	  "Portuguese Braz.": {
	    "code": "pt_BR",
	    "voice": [
	      "Raquel"
	    ],
	    "gender": [
	      "F"
	    ]
	  },
	  "Romanian": {
	    "code": "ro_RO",
	    "voice": [
	      "Simona"
	    ],
	    "gender": [
	      "F"
	    ]
	  },
	  "Russian": {
	    "code": "ru_RU",
	    "voice": [
	      "Milena"
	    ],
	    "gender": [
	      "F"
	    ]
	  },
	  "Scottish English": {
	    "code": "en_SC",
	    "voice": [
	      "Fiona"
	    ],
	    "gender": [
	      "F"
	    ]
	  },
	  "Slovak": {
	    "code": "sk_SK",
	    "voice": [
	      "Laura"
	    ],
	    "gender": [
	      "F"
	    ]
	  },
	  "South African English": {
	    "code": "en_ZA",
	    "voice": [
	      "Tessa"
	    ],
	    "gender": [
	      "F"
	    ]
	  },
	  "Spanish Castilian": {
	    "code": "es_ES",
	    "voice": [
	      "Monica",
	      "Diego"
	    ],
	    "gender": [
	      "F",
	      "M"
	    ]
	  },
	  "Spanish Mexican": {
	    "code": "es_MX",
	    "voice": [
	      "Paulina",
	      "Javier"
	    ],
	    "gender": [
	      "F",
	      "M"
	    ]
	  },
	  "Swedish": {
	    "code": "sv_SE",
	    "voice": [
	      "Alva",
	      "Oskar"
	    ],
	    "gender": [
	      "F",
	      "M"
	    ]
	  },
	  "Thai": {
	    "code": "th_TH",
	    "voice": [
	      "Narisa"
	    ],
	    "gender": [
	      "F"
	    ]
	  },
	  "Turkish": {
	    "code": "tr_TR",
	    "voice": [
	      "Cem",
	      "Aylin"
	    ],
	    "gender": [
	      "M",
	      "F"
	    ]
	  }
	}
	
	"""
	This method will make a TTS request, save the audio to a file, 
	and return the request/response
	"""
	@staticmethod
	def make_request(creds=None, desired_tts_lang=None, text=None,
					 filename=None, sample_rate=16000, nchannels=1,
					 sample_width=2, audio_type='wav'):

		if text is None:
			return None
			
		tts_req = TTSRequest(desired_tts_lang, credentials=creds)
		tts_req.sample_rate = sample_rate
		tts_req.nchannels = nchannels
		tts_req.sample_width = sample_width
		tts_req.audioType = audio_type
		
		if desired_tts_lang is not None:
			tts_req.voice = desired_tts_lang['properties']['voice']

		tts_req.synthesize_to_file(filename, text) # unicode text

		if tts_req.response.was_successful():
			print green("✓ TTS",bold=True)
		else:
			print red("× TTS",bold=True)

		return tts_req

	"""
	Pass in a language code to try to match. 
	If it doesn't exist, will ask user for it.
	"""
	@staticmethod
	def get_language_input(language_code=None):
		ret = None
		if language_code is not None:
			for (k,v) in list(TTS.Languages.items()):
				if v['code'] == language_code:
					ret = (k,v)
		if ret is None:
			lang = _get_language_input('Synthesis', TTS, default="US English")
			ret = (lang['display'],lang['properties'])
			print " "
		if len(ret[1]['voice']) > 1:
			print "The following voices are available in %s..\n" % ret[1]['code']
			i = 0
			for voice in ret[1]['voice']:
				print " [%i]  %s (%s)" % (i, voice, ret[1]['gender'][i])
				i += 1
			selection = raw_input("\nWhich voice would you like to use? ")
			if selection is None or selection.strip() == '':
				selection = "0"
			ret = (ret[0], ret[1], ret[1]['voice'][int(selection.strip())])
		else:
			ret = (ret[0], ret[1], ret[1]['voice'][0])
		ret = {
			'display': ret[0],
			'properties': {
				'code': ret[1]['code'],
				'voice': ret[2]
			}
		}
		return ret
		
	"""
	Returns the Audio Type from {wav,ogg,spx,amr,qcp,evrc}
	"""
	@staticmethod
	def get_audio_type(filename=None):
		if filename is None:
			return 'wav' # assume wav
		extension = filename[filename.rindex('.')+1:]
		ret = {
			'wav': 'wav',
			'ogg': 'speex',
			'spx': 'speex',
			'amr': 'amr',
			'mp3': 'mp3'
		}
		if extension not in ret:
			raise Exception("Bad file extension: '%s' is not supported" % extension)
		return ret[extension]
	
"""
TTS Response
"""
class TTSResponse(NDEVResponse):

	def __init__(self, response):
		super(TTSResponse,self).__init__()
		self.status_code = response.status_code
		self._parse_response(response)

"""
TTS Request 
"""
class TTSRequest(NDEVRequest):

	def __init__(self, language, credentials):
		super(TTSRequest,self).__init__(credentials=credentials)
		self.url = credentials.tts_url
		self.path = credentials.tts_endpoint
		self.language = language
		self.voice = None
		self.type = 'text'
		self.audioType = 'wav'
		self.response = None

	def build_url(self):
		ret = "%s%s?appId=%s&appKey=%s&id=%s&ttsLang=%s" % (self.url, self.path, self.app_id, self.app_key, self.requestor_id, self.language['properties']['code'])
		if self.voice is not None:
			ret += "&voice=%s" % self.voice # overrides ttsLang
		return ret

	def get_headers(self):
		headers = { 
			u"Content-Type": TTS.ContentType[self.type],
			u"Accept": self._build_header_value(TTS.Accept,self.audioType) 
		}
		return headers

	"""
	Synthesizes the given text to a file. Wants/Expects `text` to be unicode.
	"""
	def synthesize_to_file(self, outname, text):
		print "* synthesizing text..."
		start_time = time.time()
		text_to_synth = text.encode('utf-8') # unicode -> utf8
		url = self.build_url()
		hdrs = self.get_headers()
		print ""
		print " Request URL"
		print " --------------- "
		print " %s" % url
		print " "
		print " Request Headers "
		print " --------------- "
		print " Content-Type:\t%s" % hdrs['Content-Type']
		print " Accept:\t%s" % hdrs['Accept']
		print " "
		response = requests.post(url, data=text_to_synth, headers=hdrs)
		print " Making request: %f seconds, %i bytes" % ((time.time() - start_time),len(response.content))
		ret = TTSResponse(response)
		if ret.was_successful():
			if self.audioType == 'wav':
				fo = wave.open(outname, 'wb')
				fo.setframerate(self.sample_rate)
				fo.setnchannels(self.nchannels)
				fo.setsampwidth(self.sample_width)
				fo.writeframes(response.content)
				fo.close()
			else:
				f = open(outname, 'wb')
				f.write(response.content)
				f.close()
		print "\n* synthesize request complete\n"
		self.response = ret
		return ret
