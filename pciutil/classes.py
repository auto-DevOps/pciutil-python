#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   classes.py
Author:     Fasion Chan
@contact:   fasionchan@gmail.com
@version:   $Id$

Description:

Changelog:

'''

import os
import json

import pciutil

CLASSES_DATA_PATH = os.path.abspath(
    os.path.join(pciutil.__file__, '../data/pci-classes.json')
)


class PciClasses(object):

    DATA_PATH = CLASSES_DATA_PATH

    CLASSES = json.loads(open(DATA_PATH).read())

    @classmethod
    def query_item(cls, _id, dct=None):
        if not dct:
            dct = cls.CLASSES

        if not isinstance(_id, str):
            _id = '%02x' % (_id,)

        return dct.get(_id)

    @classmethod
    def query(cls, class_id=0, subclass_id=0, interface_id=0, _class=None):
        if _class is not None:
            if not isinstance(_class, int):
                _class = int(_class, 16)

            class_id, subclass_id, interface_id = [
                (_class >> (2-x) * 8) & 0xff
                for x in range(3)
            ]

        class_name = None
        subclass_name = None
        interface_name = None

        class_node = cls.query_item(class_id)
        if class_node:
            class_name = class_node['__name__']

            subclass_node = cls.query_item(subclass_id, class_node)
            if subclass_node:
                subclass_name = subclass_node['__name__']

                interface_node = cls.query_item(interface_id, subclass_node)
                if interface_node:
                    interface_name = interface_node['__name__']

        return (
            class_id,
            subclass_id,
            interface_id,

            class_name,
            subclass_name,
            interface_name,
        )
