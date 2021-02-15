"""
Your task is to use the iterative parsing to process the map file and
find out not only what tags are there, but also how many, to get the
feeling on how much of which data you can expect to have in the map.
The output should be a dictionary with the tag name as the key
and number of times this tag can be encountered in the map as value.

python mapparser.py > notags.csv
"""
try:
	import xml.etree.cElementTree as ET #optimized C implementation is faster
except ImportError:
	import xml.etree.ElementTree as ET
import pprint

def count_tags(filename):
    tags = {}
    for event, elem in ET.iterparse(filename):
        if elem.tag not in set(tags.keys()):
			tags[elem.tag] = 1
			elem.clear()
        else:
			tags[elem.tag] += 1
			elem.clear()
    return tags
               
			   
def test():

    tags = count_tags('sample.osm')
    pprint.pprint(tags)
    

if __name__ == "__main__":
    test()