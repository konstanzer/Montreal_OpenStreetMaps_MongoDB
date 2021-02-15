#!/usr/bin/python
# -*- coding: utf-8 -*-
'''This combines data.py and audit.py from the example to output an updated JSON file in one step, no pprint'''
import xml.etree.cElementTree as ET
import re
import json
import io

in_file = ['sample.osm', 'montreal.osm']

problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
street_type_reFr = re.compile(r'^\b\S+\.?', re.IGNORECASE)

CREATED = ["version", "changeset", "timestamp", "user", "uid"]

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
                refs.append(child.attrib.get('ref'))
            if child.attrib.get('k'):
				if problemchars.search(child.attrib.get('k')):
					continue
				elif child.attrib.get('k') == "addr:street":
					address[u"street"] = audit_street(child.attrib.get(u'v'))
				elif child.attrib.get('k').startswith("addr:") and ":" not in child.attrib.get('k')[5:]: #True if there is no second colon
					address[child.attrib.get('k')[5:]] = child.attrib.get('v')
				else:
					node[child.attrib.get('k')] = child.attrib.get(u'v')

        if address != {}:
            node[u'address'] = address
        if refs != []:
            node[u'node_refs'] = refs
            
        return node
    
    else:
        return None
            
#updates last word if not in 'expected' and first word if not in 'expectedFr' using the mapping dictionary      
def audit_street(name):
	m = street_type_re.search(name) #matches last word
	n = street_type_reFr.search(name) #matches first word
	if m and m.group() not in expected and n and n.group() not in expectedFr:
		new_name = u''
		for word in name.split(" "):
			if word in mapping.keys():
				word = mapping[word]
			new_name = new_name + ' ' + word
		
		try:
			return new_name.strip()
		except UnicodeEncodeError: #if new_name returns unicode encoding error, the original name is kept
			return name
	else:
		return name

		
def process_map(file_in):
    file_out = "{0}.json".format(file_in)
    data = []
    with io.open(file_out, "w", encoding='utf-8') as fo: #opens new file with utf-8 encoding to handle non-ASCII French
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
				data.append(el)
				fo.write(json.dumps(el, ensure_ascii=False) + "\n") #writes el as unicode
				element.clear()
    return data

if __name__ == "__main__":
    process_map(in_file[0])
