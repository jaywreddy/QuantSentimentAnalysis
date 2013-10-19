from parser import parser
import json

#load all items in raw
import os
path = 'stream/raw_scrape/'
listing = os.listdir(path)
for fi in listing:
	f = open('stream/raw_scrape/'+fi, 'r')
	articles = json.load(f)
	processed = []
	for article in articles:
		processed.append(parser.format(article))

	f.close()

	f2 = open('cleaned/'+f.name, 'w')
	json.dump(f2, processed)

