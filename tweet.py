from twitter import *
import re
import json
import datetime
import time
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

hashtags = []
currentTime = time.time()
endTime = time.time() + 600
# Print each tweet in the stream to the screen 
# Here we set it to stop after getting 1000 tweets. 
# You don't have to set it to stop, but can continue running 
# the Twitter API to collect data for days or even longer. 
def collectStream(iterator,tweets_filename):
    tweets_file = open(tweets_filename, "w")
    #tweet_count = 10000
    
    for tweet in iterator:
        #tweet_count -= 1
    # Twitter Python Tool wraps the data returned by Twitter 
    # as a TwitterDictResponse object.
    # We convert it back to the JSON format to print/score
        tweets_file.write(json.dumps(tweet))
        tweets_file.write('\n')
    
    # The command below will do pretty printing for JSON data, try it out
    # print json.dumps(tweet, indent=4)
        currentTime = time.time()
        if currentTime >= endTime:
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
                
                for hashtag in tweet['entities']['hashtags']:
                    tweets_clean_file.write(hashtag['text'])
                    tweets_clean_file.write('\n')

        except:
            # read in a line is not in JSON format (sometimes error occured)
            continue

def readHashtagFile(tweets_clean_filename):
    with open(tweets_clean_filename) as file:
        for line in file:
            line = line.strip()
            hashtags.append(line)

collectStream(iterator,tweets_filename)
cleanStream(tweets_filename)
tweets_clean_filename = 'cleanStream.txt'
readHashtagFile(tweets_clean_filename)
print Counter(hashtags).most_common()[:10]
#print ('\n'.join(map(str, hashtags)))