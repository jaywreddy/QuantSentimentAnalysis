from multiprocessing import Process, Queue, Pool
from scraper import stream
import json
from text.blob import TextBlob
import unicodedata
from datetime import datetime

#starts scraper in separate thread
q = Queue()
p = Process(target= stream, args= (q, 'apple'))
p.start()

processes = 3

pool = Pool(processes)

def process_tweet(q):
        while True:
            tweet= json.loads(q.get())
            text  = tweet['text']
            processed = unicodedata.normalize('NFKD', text).encode('ascii','ignore')
            timestamp = tweet['created_at']
            created_at = datetime.strptime(timestamp, '%a %b %d %H:%M:%S +0000 %Y')
            utc_timestamp = created_at.strftime("%s")
            #parse
            score = TextBlob(processed).sentiment[0]
            f =open('database.txt', 'a')
            f.write(str((score, utc_timestamp))+'\n')    

for i in range(processes):
        Process(target = process_tweet, args=tuple([q])).start()
 
