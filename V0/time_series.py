import datetime
from scipy import stats

def time_series(term):
	sentiment_time_series = []
	for article in articles:
		if term in article['terms']:
			sentiment_time_series.append((article['last_updated'], article['sentiment']))
	return sentiment_time_series


def sort_data(term):
	#load from all sources, choose only the sources which contain stuff
	path = 'cleaned/'
	listing = os.listdir(path)
	articles = []
	for fi in listing:
		f = open('stream/raw_scrape/'+fi, 'r')
		articles += json.load(f)	
		f.close()
	return [(art['sentiment'], art['last_update']) for art in articles if term in art['terms']]

def format_stock(time_series):
	close = time_series['Series']['Close']
	op = time_series['Series']['Open']
	dates = time_series['Timestamp']
        diff = []
	for i in range(len(close)):
		d = op(i)-close(i)
		time = datetime.strptime(dates[i], "%a, %d %b %Y %H:%M:%S %Z")
                time = time+ timedelta(hours = 16) #takes it from the beginning of the day to the middle of trading
		diff.append((d,time))

def calculate_correlation(stock, sentiment):
	#both in form of (time, value)
	#transform into equal length lists of time values.
	sortedtime = sorted(time, lambda x: x[0])
	sortedsent = sorted(sentiment, lambda x:x[0]) # convert to UTC for sorting
	mintime = x[0][0]
	maxtime = x[-1][0]

	#convert mintime to hours, take diff to 21:00, that's our starting date
	sentlist = []
	for (time, sentiment) in sortedtime:
		locallist = []
		d = date.fromtimestamp(time)
		if d.hour<21 and d.hour>14 and (d.min>30 or d.hour !=14)
			locallist.append((time, sentiment))
		else: 
			if len(locallist) !=0:
				sentlist.append(locallist)
	stocklist = []
	for (time, value) in stock:
		if time>sentlist[0][0][0] and len(stocklist)!=len(sentlist):
			stocklist.append((time,value))

	if len(stocklist) < len(sentlist):
		sentlist = sentlist[0:-1]
	
	return stats.pearsonr(sentlist, stocklist)
	
