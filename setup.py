#!/usr/bin/env python

from setuptools import setup

setup(name='newest',
      version='0.1',
      description='Automatically installs package upgrades',
      author='Lars Jørgen Solberg',
      author_email='supersolberg@gmail.com',
      url='https://github.com/larsjsol/newest',
      packages=['newest'],
      install_requires=['pyzmq']
      )