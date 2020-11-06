from setuptools import setup
from os import path
import sys

if sys.version_info < (3, 6):
    sys.exit('Sorry, Python < 3.6 is not supported')

here = path.abspath(path.dirname(__file__))

setup(
    name="sels8s",
    packages=["sels8s"]
    )
