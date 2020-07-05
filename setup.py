#!/usr/bin/env python3

from setuptools import setup

requirements = open("requirements.txt", 'r').read().split("\n")

setup(
    name='tsteno',
    version='0.1',
    description='A useful module',
    author='A free, light-weight alternative to Mathematica.',
    author_email='hola@hosecarlos.me',
    packages=['tsteno'],
    install_requires=requirements,
)
