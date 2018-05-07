#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   setup.py
Author:     Fasion Chan
@contact:   fasionchan@gmail.com
@version:   $Id$

Description:

Changelog:

'''

from setuptools import (
    setup,
)

setup(
    name='pciutil',
    author='Fasion Chan',
    author_email='fasionchan@gmail.com',
    packages=[
        'pciutil',
    ],
    package_data={
        'pciutil': [
            'data/pci-classes.json',
            'data/pci.ids.gz',
        ],
    },
)
