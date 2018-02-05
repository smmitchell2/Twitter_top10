#!/usr/bin/python

#-----------------------------------------------------------------------
# twitter-trends
#  - lists the current global trending topics
#-----------------------------------------------------------------------
import json
import datetime

from twitter import *

class tweetClass:
    name = ""
    count = ""

    def __init__(name,count):
        self.name = name
        self.count = count

#-----------------------------------------------------------------------
# load our API credentials 
#-----------------------------------------------------------------------
config = {}
execfile("config.py", config)

#-----------------------------------------------------------------------
# create twitter API object
#-----------------------------------------------------------------------
twitter = Twitter(
		        auth = OAuth(config["access_key"], config["access_secret"], config["consumer_key"], config["consumer_secret"]))


#-----------------------------------------------------------------------
# retrieve global trends.
# other localised trends can be specified by looking up WOE IDs:
#   http://developer.yahoo.com/geo/geoplanet/
# twitter API docs: https://dev.twitter.com/rest/reference/get/trends/place
#-----------------------------------------------------------------------

#it finds top 50 in 24hrs in random order
results = twitter.trends.place(_id = 1)

print "World Trends"
top_trends = []
lowest_count = 0
for location in results:
	for trend in location["trends"]:
		print " - %s %s" % (trend["name"],trend["tweet_volume"])
#print(top_trends)
"""
 if top_trends.count == 0:
            tw = tweetClass(trend["name"],trend["tweet_volume"])
            top_trends.append(tw)
            lowest_count = int(trend["tweet_volume"])
        else:
            if int(trend["tweet_volume"]) >= lowest_count:
                tw = tweetClass(trend["name"],trend["tweet_volume"])
                top_trends.append(tw)
"""