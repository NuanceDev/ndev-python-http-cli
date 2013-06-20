import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

# if sys.version_info < (2, 6): json?

setup(

      name = "ndevutils",
      version = "0.1",

      description = """Interactive utilities for developers using the NDEV HTTP service.""",
      long_description = read('README.md'),

      url = "", # TODO: add github URL

      author = "Nuance Communications, Inc.",
      author_email = "nirvana.tikku@nuance.com",

      packages = find_packages(),

      install_requires = [
           "pyaudio",
           "requests == 1.2.0",
           "scikits.samplerate",
      ],

      classifiers = [ 
           'Development Status :: 4 - Beta',
           'Programming Language :: Python',
           'Intended Audience :: Developers',
           'Environment :: Console',
           'Topic :: Utilities',
      ],

)
