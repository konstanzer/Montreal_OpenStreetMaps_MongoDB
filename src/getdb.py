import gridfs
import json

def insert_data(data, db):
    # Insert the data into a collection 'osm'
	db.osm.insert(data)

if __name__ == "__main__":
    
    from pymongo import MongoClient
    client = MongoClient("mongodb://localhost:27017") #could also be 'localhost', 27017 or empty
    db = client.osmdata

    with open('montreal.osm.json') as f:
		for line in f:
			data = json.loads(line) #loads JSON line by line because it's not , delimited
			insert_data(data, db)
		print db.osm.find_one()