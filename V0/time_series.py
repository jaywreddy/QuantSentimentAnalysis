

def time_series(term):
	sentiment_time_series = []
	for article in articles:
		if term in article['terms']:
			sentiment_time_series.append((article['last_updated'], article['sentiment']))
	return sentiment_time_series



def calculate_correlation(stock, sentiment):
	#both in form of (time, value)
	#transform into equal length lists of time values.

	#get min, max times on the sentiment

	#sum all complete days in range on both values.

	mintime = 

	maxtime= 


#steps: get time series data, coerce sentiment into time series format. 
	
	
