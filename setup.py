from setuptools import setup
from os import path
import sys

if sys.version_info < (3, 6):
    sys.exit('Sorry, Python < 3.6 is not supported')

here = path.abspath(path.dirname(__file__))

with open("README.md", "r") as fh:
    long_description = fh.read()

requires = [
    'requests==2.24.0',
    'keystoneauth1==3.17.1',
    'python-keystoneclient==3.21.0'
]

setup(
    name="sels8s",
    version="1.0.2",
    author_email="sls@selectel.ru",
    description="SDK for python serverless functions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/selectel/serverless-python",
    packages=["sels8s"],
    install_requires=requires
    )
