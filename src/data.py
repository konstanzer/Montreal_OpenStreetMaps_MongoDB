#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
from pprint import pprint
import re
import codecs
import json
import io
"""
Your task is to wrangle the data and transform the shape of the data
into the model we mentioned earlier. 

You have to complete the function 'shape_element'.
We have provided a function that will parse the map file, and call the function with the element
as an argument. You should return a dictionary, containing the shaped data for that element.
We have also provided a way to save the data in a file, so that you could use
mongoimport later on to import the shaped data into MongoDB. You could also do some cleaning
before doing that, like in the previous exercise, but for this exercise you just have to
shape the structure.

In particular the following things should be done:
- you should process only 2 types of top level tags: "node" and "way"
- all attributes of "node" and "way" should be turned into regular key/value pairs, except:
    - attributes in the CREATED array should be added under a key "created"
    - attributes for latitude and longitude should be added to a "pos" array,
      for use in geospacial indexing. Make sure the values inside "pos" array are floats
      and not strings. 
- if second level tag "k" value contains problematic characters, it should be ignored
- if second level tag "k" value starts with "addr:", it should be added to a dictionary "address"
- if second level tag "k" value does not start with "addr:", but contains ":", you can process it
  same as any other tag.
- if there is a second ":" that separates the type/direction of a street,
  the tag should be ignored
"""

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = ["version", "changeset", "timestamp", "user", "uid"]


def shape_element(element):
    node = {}
    if element.tag == "node" or element.tag == "way":
        node["type"] = element.tag
        create = {}
        lat, lon = float(), float()
        address = {}
        refs = []
        for key in element.keys():
            if key in CREATED:
                create[key] = element.get(key)
            elif key == "lat":
                lat = element.get(key)
            elif key == "lon":
                lon = element.get(key)
            else:
                node[key] = element.get(key)
        
        if lat != 0.0: #only writes lat and lon if a value exists
            node[u"pos"] = [lat, lon]
        if create != []:
			node[u"created"] = create
        
        for child in element: #looks for subelements
            if child.attrib.get('ref'):
                refs.append(child.attrib.get(u'ref'))
            if child.attrib.get('k'):
                if problemchars.search(child.attrib.get('k')):
                    continue
                if child.attrib.get('k').startswith("addr:"):
                    if ":" not in child.attrib.get('k')[5:]: #True if there is no second colon
                        address[child.attrib.get(u'k')[5:]] = child.attrib.get(u'v')
                    continue
                node[child.attrib.get(u'k')] = child.attrib.get(u'v')

        if address != {}:
            node[u'address'] = address
        if refs != []:
            node[u'node_refs'] = refs
            
        return node
    
    else:
        return None
            
            
def process_map(file_in):
    file_out = "{0}2.json".format(file_in)
    data = []
    with io.open(file_out, "w", encoding='utf-8') as fo: #opens new file with utf-8 encoding to handle non-ASCII French
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
				data.append(el)
				fo.write(json.dumps(el, indent=2, ensure_ascii=False) + "\n") #remove indent attribute to reduce file size
				element.clear()
    return data

if __name__ == "__main__":
    process_map('sample.osm')
	#process_map('montreal.osm')
