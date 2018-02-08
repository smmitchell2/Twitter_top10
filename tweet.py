from twitter import *
import re
import json
import datetime
from collections import Counter


#-----------------------------------------------------------------------
# load our API credentials 
#-----------------------------------------------------------------------
config = {}
execfile("config.py", config)

#-----------------------------------------------------------------------
# create twitter API object
#-----------------------------------------------------------------------
auth = OAuth(config["access_key"], config["access_secret"], config["consumer_key"], config["consumer_secret"])
stream = TwitterStream(auth = auth, secure = True)

# Initiate the connection to Twitter Streaming API
twitter_stream = TwitterStream(auth=auth)

# Get a sample of the public data following through Twitter
iterator = twitter_stream.statuses.sample()

tweets_filename = 'stream.txt'
tweets_file = open(tweets_filename, "r")

# Print each tweet in the stream to the screen 
# Here we set it to stop after getting 1000 tweets. 
# You don't have to set it to stop, but can continue running 
# the Twitter API to collect data for days or even longer. 
def collectStream(iterator,tweets_file):
    tweet_count = 1000
    for tweet in iterator:
        tweet_count -= 1
    # Twitter Python Tool wraps the data returned by Twitter 
    # as a TwitterDictResponse object.
    # We convert it back to the JSON format to print/score
        print json.dumps(tweet)  
    
    # The command below will do pretty printing for JSON data, try it out
    # print json.dumps(tweet, indent=4)
       
        if tweet_count <= 0:
            break

def cleanStream(tweets_filename):
    tweets_clean_filename = 'cleanStream.txt'
    tweets_filename = 'stream.txt'
    tweets_file = open(tweets_filename, "r")
    tweets_clean_file = open(tweets_clean_filename,"w")

    for line in tweets_file:
        try:
            # Read in one line of the file, convert it into a json object 
            tweet = json.loads(line.strip())
            if 'text' in tweet: # only messages contains 'text' field is a tweet
                #print tweet['id'] # This is the tweet's id
                #print tweet['created_at'] # when the tweet posted
                #tweets_clean_file.write('\n')
                #tweets_clean_file.write(tweet['text']) # content of the tweet
                #tweets_clean_file.write('\n')
                hashtags = []
                for hashtag in tweet['entities']['hashtags']:
                    tweets_clean_file.write('#'+hashtag['text'])
                    tweets_clean_file.write('\n')
            	    hashtags.append(hashtag['text'])
                #print(Counter(hashtags).most_common()[:10])
                #tweets_clean_file.write('#' + hashtags)
                print(Counter(hashtags).most_common()[:10])

        except:
            # read in a line is not in JSON format (sometimes error occured)
            continue

collectStream(iterator,tweets_file)
cleanStream(tweets_filename)