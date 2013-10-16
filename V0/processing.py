from multiprocessing import Process, Queue
from scraper import stream
import json
from text.blob import TextBlob
import unicodedata
#starts scraper in separate thread
q = Queue()
p = Process(target= stream, args= (q, 'apple'))
p.start()

while True:
    tweet= json.loads(q.get())
    text  = tweet['text']
    processed = unicodedata.normalize('NFKD', text).encode('ascii','ignore')
    timestamp = tweet['created_at']
    #parse
    score = TextBlob(processed).sentiment[0]
    print(score, timestamp)     
