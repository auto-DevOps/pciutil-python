#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   demo.py
Author:     Fasion Chan
@contact:   fasionchan@gmail.com
@version:   $Id$

Description:

Changelog:

'''

from pciutil.classes import (
    PciClasses,
)

print(PciClasses.query(class_id=0x02))
