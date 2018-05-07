#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   ids.py
Author:     Fasion Chan
@contact:   fasionchan@gmail.com
@version:   $Id$

Description:

Changelog:

'''

import gzip
import os

from collections import (
    defaultdict,
)

tree = lambda: defaultdict(lambda: tree())


class PciIds(object):

    '''
        # Syntax:
        # vendor  vendor_name
        #       device  device_name                             <-- single tab
        #               subvendor subdevice  subsystem_name     <-- two tabs
    '''

    PCI_IDS_PATH = '/usr/share/misc/pci.ids'

    @staticmethod
    def _ensure_numberic(n):
        if isinstance(n, str):
            if not n:
                return
            return int(n, 16)

        return n

    @classmethod
    def load_from_file(cls, filepath=PCI_IDS_PATH):
        open_file = open
        if filepath.endswith('.gz'):
            open_file = gzip.open
        lines = open_file(filepath, 'rt').readlines()
        return cls(lines=lines)

    @classmethod
    def smart_load(cls):
        for path in (
            os.path.abspath(os.path.join(__file__, '../data/pci.ids.gz')),
            '/usr/share/misc/pci.ids',
            '/usr/share/hwdata/pci.ids',
        ):
            if os.path.exists(path):
                return cls.load_from_file(filepath=path)

    def __init__(self, lines):
        self.mapping = tree()

        for line in lines:
            line = line.rstrip()
            if not line:
                continue

            if line.startswith('#'):
                continue

            if line.startswith('\t\t'):
                subvendor, subdevice, subsystem_name = line.strip().split(' ', 2)
                subvendor = self._ensure_numberic(subvendor)
                subdevice = self._ensure_numberic(subdevice)

                device_node[subvendor][subdevice] = subsystem_name.strip()
                continue

            if line.startswith('\t'):
                device, device_name = line.strip().split(' ', 1)
                device = self._ensure_numberic(device)

                device_node = vendor_node[device]
                device_node['__name__'] = device_name.strip()
                continue

            vendor, vendor_name = line.split(' ', 1)
            vendor = self._ensure_numberic(vendor)

            vendor_node = self.mapping[vendor]
            vendor_node['__name__'] = vendor_name.strip()

    def query(self, vendor, device, subsystem_vendor, subsystem_device):
        vendor_node = self.mapping[vendor]
        vendor = vendor_node['__name__'] or None

        device_node = vendor_node[device]
        device = device_node['__name__'] or None

        subsystem_name = device_node[subsystem_vendor][subsystem_device] or None

        return vendor, device, subsystem_name

    def __getitem__(self, key):
        return self.mapping[key]
