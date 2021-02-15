#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
"""
Before you process the data and add it into MongoDB, you should
check the "k" value for each "<tag>" and see if they can be valid keys in MongoDB,
as well as see if there are any other potential problems.

As we saw in the quiz earlier, we would like to change the data model
and expand the "addr:street" type of keys to a dictionary like this:
{"address": {"street": "Some value"}}
So, we have to see if we have such tags, and if we have any tags with problematic characters.
"""

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


def key_type(element, keys):
    if element.tag == "tag":
        if lower.match(element.get('k')):
            keys['lower'] += 1
        elif lower_colon.match(element.get('k')):
            keys['lower_colon'] += 1
        elif problemchars.search(element.get('k')):
            keys['problemchars'] += 1
        else: keys['other'] += 1
            
    return keys


def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys


def test():
    keys = process_map('montreal.osm')
    pprint.pprint(keys)
 

if __name__ == "__main__":
    test()
