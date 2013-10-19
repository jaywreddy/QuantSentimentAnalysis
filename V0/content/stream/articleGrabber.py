#A utility for getting a Pulse article stream
import httplib, urllib, urllib2,base64, json, time
from multiprocessing import *
from multiprocessing.queues import *

PROCESSES=5 #number of helper daemons to buffer articles

SCRAPE = ['Entrepreneurship & Small Business', ]


rss_url="hr-pulsesubscriber.appspot.com"

def exponential_backoff(func):
	def exponential(*args):
		count=.25
		for i in range(8):
			try:
				return func(*args)
			except Exception as e:
				print "Exception encountered in ArticleGrabber: "+str(e)+" url: "+ str(args)

				time.sleep(count)
				count *= 2
				continue
			break
	return exponential

@exponential_backoff
def get_sources():
	url="/api/v2/catalog/catalog_items?url_to_title_and_collection_map=true"
	conn=httplib.HTTPConnection("www.pulse.me")
	conn.request("GET",url)
	response=conn.getresponse()
	message=json.load(response)
	return message['data']

@exponential_backoff
def get_articles(source, last_update_time):
	articles=[]
	query= source+"&last_updated="+str(last_update_time)
	response=urllib2.urlopen(query)
	try:
		message=json.load(response)
		art= message['responseData']['feed']['entries']
		if art:
			articles=art
	except ValueError:
		pass
	if articles:
		return articles
	return []

def get_articles_back(source, start_time, end_time):
	articles = []
        last_time = start_time
        while last_time > end_time:
		query = source+ "&last_story_published="+str(start_time)+"&last_story_updated="+str(last_time)
		response=urllib2.urlopen(query)
                message = json.load(response)
                art= message['responseData']['feed']['entries']
                articles += art
                last_time = articles[-1]['last_updated']
		print(len(articles))
        return articles

def streaming_articles():
	article_queue=Queue()
	source_queue=Queue()
	sources=get_sources()
	for source in sources:
		source_queue.put((source, 0))
	for i in range(PROCESSES):
		p=Process(target=worker, args=(source_queue, article_queue))
		p.start()
	while True:
		yield article_queue.get()
	


def worker(source_queue, article_queue):
	while True:
		(source, last)=source_queue.get()
		articles=get_articles(source, last)
		if articles:
			for article in articles:
				article_queue.put(article)

		
			last=articles[0]['last_updated']
		source_queue.put(source, last)

def get_target_sources():
        source_file = open('TargetSources.txt', 'r')
        target_sources = json.load(source_file)
	raw_sources = get_sources()
        links={}
        for i in range(len(raw_sources)):
		if raw_sources.values()[i][0] in target_sources:
			links[raw_sources.values()[i][0]]= raw_sources.keys()[i]
	return links



def build_archive(past_date):
	curr_time = time.mktime(time.gmtime())
        sources = list(get_target_sources().items())
        def archive_source((title, link)):
		arts =get_articles_back(link, curr_time, past_date)
           	store = open('raw_scrape/'+title+'.txt', 'w')
                json.dump(arts,store)
		store.close()
                print(title + ' completed')
		return None

	for source in sources:
		archive_source(source)
		
		
"""
#Code for logging into a specific account


device_id= 'linux_workstaton_1'
device_name = 'linkedin_workstation'
login_url= "/api/v2/basic_api_token"
source_url= "/api/source_sync"
all_source_url="/api/source_sync"


def login(self, username="jreddy", password="3D4am12mqt41"):
	conn=httplib.HTTPConnection("www.pulse.me")
	params= urllib.urlencode({'device_id': device_id, 'device_name': device_name})
	url=login_url+"?"+params
	base64string= base64.encodestring('%s:%s'% (username, password))
	headers = {'Authorization': "Basic %s" % base64string}
	conn.request("GET", url,"",headers)
	response= self.conn.getresponse()
	message= json.load(response)
	token= message['data']['token']

def getSources(self):
	params= urllib.urlencode({'api_token': self.token})
	url=source_url+"?"+params
	self.conn.request("GET",url)
	response= self.conn.getresponse()
	message= json.load(response)
	sources=[]
	for page in message['data']['pages']:
			#looping through categories
			#print page['page_title']
		for source in page['sources']:
				#print "     "+source['source_title']
			sources.append(source['source_url'])
	return sources

def getArticles(self):
	sources= self.getSources()
	articles=[]
	for feed_url in sources:
		feed_url=feed_url.split('?')[1]
		connection= httplib.HTTPConnection(rss_url)
		query= "/items"+"?"+feed_url
			#if len(source_articles)>0:
			#	last_entry= source_articles[len(source_articles)-1]
			#	time=last_entry['last_updated']
			#	query=query+"&last_story_published="+str(time)
		connection.request("GET",query)
		response=connection.getresponse()
		try:
			message=json.load(response)
			articles+=message['responseData']['feed']['entries']
		except ValueError:
			print "JSON parsing error in response. Continuing."
			pass
	return articles


"""

