from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

# Go to http://dev.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key="eH3tPK3JMqo0Vn4Dtyle2g"
consumer_secret="kP3Ar0QuiUUDELIG6xccUtnWITA0BmIjv6Fkj8BXo"

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token="1507356518-YLDCmnyUWw7pu4I1SYUO940ZKTfvUC74beQjJ8u"
access_token_secret="HtbRxhjygvgjXJw4p6I7lyWP9BPatEc4Oc4Gzf8w"

class StdOutListener(StreamListener):
    """ A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.

    """

    def __init__(self, buff):
        self.buff = buff
    def on_data(self, data):
        self.buff.put(data)

    def on_error(self, status):
        print status


def stream(buff, terms):
    l = StdOutListener(buff)
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    stream.filter(track=[terms])
