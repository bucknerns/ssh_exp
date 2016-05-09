import sys
from setuptools import setup


setup(
    name = "paramiko",
    version = "0.0.1",
    description = "SSH2 client library",
    url = "https://github.com/paramiko/paramiko/",
    packages = ['paramiko'],
    install_requires=[
        'cryptography>=1.1',
        'pyasn1>=0.1.7',
    ],
)
