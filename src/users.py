#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
"""
The first task is a fun one - find out how many unique users
have contributed to the map in this particular area!
The function process_map should return a set of unique user IDs ("uid")
"""

def process_map(filename):
    users = []
    for _, element in ET.iterparse(filename):
        user = element.attrib.get('uid')
        
        if user not in set(users) and user != None:
			users.append(user)
			element.clear()
			
    return users

def test():

    users = process_map('montreal.osm')
    pprint.pprint(users)
   
if __name__ == "__main__":
    test()
