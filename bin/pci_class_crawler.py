#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   pci_class_crawler.py
Author:     Fasion Chan
@contact:   fasionchan@gmail.com
@version:   $Id$

Description:

Changelog:

'''

import json
import re
import requests

from collections import (
    OrderedDict,
)

root_uri = 'https://pci-ids.ucw.cz/read/PD'

TABLE_MOD = re.compile('>([^<]*)</a><td>([^<]*)<td>')


def fetch_classes(uri, classes=None):
    if classes is None:
        classes = OrderedDict()

    content = requests.get(uri).content
    #print(content)
    for line in content.split('\n'):
        line = line.strip()
        if not line.startswith('<tr class="item">'):
            continue

        records = TABLE_MOD.findall(line)
        for value, name in records:
            value, name = value.strip(), name.strip()

            subclasses = classes.setdefault(value, OrderedDict())
            subclasses['__name__'] = name

        if '<a ' in line:
            fetch_classes(
                uri=uri+'/'+value,
                classes=subclasses,
            )

        #print(line)

    return classes


if __name__ == '__main__':
    classes = fetch_classes(root_uri)
    classes_jsonic = json.dumps(
        classes,
        ensure_ascii=False,
        indent=4,
    )
    print(classes_jsonic)
