import nltk
import time
from multiprocessing import *
from text.blob import TextBlob

PROCESSES= 5 #number of NLTK parser daemons

def ascii(text):
	return "".join(char for char in text if ord(char)<128)

def generate_set(article):
	article=nltk.clean_html(article)
	chunked_sentences=  nltk_preprocess(article)
	entity_names=[]
	for tree in chunked_sentences:
		entity_names.extend(extract_entity_names(tree))
	return set(entity_names)


"""nltk_preprocess and extract_entity_names from onyxfish/example1.py on github"""
def nltk_preprocess(article):
	sentences = nltk.sent_tokenize(article)
	tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
	tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
	chunked_sentences = nltk.batch_ne_chunk(tagged_sentences, binary=True)
	return chunked_sentences

def extract_entity_names(t):
	entity_names = []
	if hasattr(t, 'node') and t.node:
		if t.node == 'NE':
			name=' '.join([child[0] for child in t])
			name=ascii(name)
			name=str(name).lower() #standardize format for matching
			entity_names.append(name)
		else:
			for child in t:
				entity_names.extend(extract_entity_names(child))
	return set(entity_names)

def format(article):
		if 'content' in article:
			content= article['content']
		else:
			return
		last_updated= article['created']
		terms= generate_set(content)
		title="No title"
		try:
			title= ascii(article['title'])
		except KeyError:
			pass
		content_strip = str(ascii(content)).lower()
		term_freq={}
		for term in terms:
			term_freq[term]=content_strip.count(term)

		score = get_sentiment(content_strip)
		print("Parsed: "+ title)
		return {'terms':term_freq,'title':title, 'last_update':last_updated, 'sentiment': get_sentiment(score)}

def get_sentiment(text):
	score = TextBlob(str(text)).sentiment[0] #ignore subjectivity
	return score


def init_parser():
	work_queue=Queue()
	done_queue=Queue()
	def insert(stream):
		while True:
			work_queue.put(stream.next())

	def out():
		while True:
			yield done_queue.get()


	for i in range(PROCESSES):
		p=Process(target=worker, args=(work_queue, done_queue))
		p.start()
	return (insert, out)
	

def worker(work_queue, done_queue):
	while True:
		article=work_queue.get()
		formatted= format(article)
		if formatted:
			done_queue.put(formatted)
