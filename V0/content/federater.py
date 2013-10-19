from stream.articleGrabber import *
from parser.parser import *
from stream import articleGrabber
from parser import parser

PROCESSES=1 #number of workers loading in articles to parse
pro=[]

def federater():
	stream=streaming_articles()
	(parse_in, parse_out)=init_parser()
	for i in range(PROCESSES):
		p=Process(target=worker, args=(stream, parse_in))
		p.start()
	while True:
		 yield parse_out().next()

def worker(stream, parse):
	parse(stream)
