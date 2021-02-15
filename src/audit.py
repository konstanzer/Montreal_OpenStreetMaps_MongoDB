#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Update street names with mapping dict and list the weirdos as a set.
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

osm_file = open("sample.osm", "r")

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
street_type_reFr = re.compile(r'^\b\S+\.?', re.IGNORECASE)
lower = re.compile(r'^([a-z]|_)*$')

street_types = defaultdict(set)

expectedFr = ["Cercle", "Rue", "Impasse", "Autoroute", "Lane", "Road", "Street", "Avenue", "Jardins", "Square", "Ruelle", "Passage", "Boulevard", "Villa", "Route", "Place", "Chemin", "Croissant", "Terrasse", u"Allée", u"Carré", u"Cité", u"Montée", "Rang", u"Côte"]
expected = ["Street", "Crescent", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", "Trail", "Parkway", "Commons"]

mapping = { "St": "Street", 
			"St.": "Street", 
			"Rd": "Road", 
			"Rd.": "Road", 
			"Ave": "Avenue", 
			"Ave.": "Avenue",
			"Rte": "Route",	
			"Hwy.": "Highway", 
			"Hwy": "Highway", 
			"Pkwy": "Parkway", 
			"PKWY": "Parkway",
			"rang": "Rang",
			"cercle": "Cercle",
			u"côte": u"Côte", 
			"cote": u"Côte", 
			"Cote": u"Côte",
			"O.": "Ouest", 
			"O": "Ouest", 
			"N.": "N", 
			"E.": "E", 
			"est": "Est", 
			"ouest": "Ouest", 
			"nord": "Nord",
			"sur": "Sur",
			"S.": "S", 
			"W": "West", 
			"W.": "West",
			"Av": "Avenue",
			"Av.": "Avenue",
			"av": "Avenue",
			"av.": "Avenue", 
			"ave": "Avenue",
			"avenue": "Avenue",
			"Ch": "Chemin",
			"Ch": "Chemin",
			"ch": "Chemin",
			"ch.": "Chemin",
			"chemin": "Chemin",
			"Boul": "Boulevard",
			"Boulvard": "Boulevard",
			"Boul.": "Boulevard",
			"Blvd": "Boulevard",
			"Blvd.": "Boulevard",
			"boul": "Boulevard",
			"boul.": "Boulevard",
			"blvd": "Boulevard", 
			"bd": "Boulevard", 
			"Bd": "Boulevard", 
			"Bd.": "Boulevard",
			"blvd.": "Boulevard",
			"boulevard": "Boulevard",
			"St": "Saint",
			"St.": "Saint",
			"rue": "Rue",
			"Ste-Catherine": "Sainte-Catherine"}

#updates last word if not in 'expected' and first word if not in 'expectedFr' using the mapping dictionary      
def audit_street_type(street_types, name):
	m = street_type_re.search(name) #matches last word
	n = street_type_reFr.search(name) #matches first word
	if m and m.group() not in expected and n and n.group() not in expectedFr:
		street_types[n.group()].add(name)
		

def update_name(name):
	name = name.split(" ")
	new_name = ''
	for word in name:
		if word in mapping.keys():
			word = mapping[word]
		new_name = new_name + ' ' + word
			
	return new_name.strip()
	

def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

	
def audit():
	for event, elem in ET.iterparse(osm_file, events=("start",)):
		if elem.tag == "node" or elem.tag == "way":
			for tag in elem.iter("tag"):
				if is_street_name(tag):
					audit_street_type(street_types, tag.attrib['v'])
	return street_types

	
def test():
	st_types = audit()
	pprint.pprint(dict(st_types))
	for st_type, ways in st_types.iteritems():
		for name in ways:
			better_name = update_name(name)
			print name, "=>", better_name


if __name__ == '__main__':
    test()	