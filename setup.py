import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

# if sys.version_info < (2, 6): json?

setup(

      name = "ndevutils",
      version = "0.1",

      description = """Interactive utilities for developers using the NDEV HTTP service.""",
      long_description = read('README.md'),

      url = "https://github.com/NuanceDev/ndev-python-http-cli",

      author = "Nuance Communications, Inc.",
      author_email = "nirvana.tikku@nuance.com",

      packages = find_packages(),

      dependency_links = [
           "http://people.csail.mit.edu/hubert/pyaudio/packages/pyaudio-0.2.8.tar.gz#egg=pyaudio",
      ],
      install_requires = [
           "numpy",
           "pyaudio",
           "scikits.samplerate",
           "requests>=1.2.0",
      ],

      classifiers = [
           'Development Status :: 4 - Beta',
           'Programming Language :: Python',
           'Intended Audience :: Developers',
           'Environment :: Console',
           'Topic :: Utilities',
      ],

)
