import config
from sys import argv
import tweepy
from tweepy import OAuthHandler, Stream
import json
import hashtagListener

# create your own config.py file then define your own twitter API credentials
auth = OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_secret)

api = tweepy.API(auth)

streamListener = hashtagListener.HashtagListener(time_limit=60)
twitter_stream = tweepy.Stream(auth = api.auth, listener = streamListener)

# twitter_stream = Stream(auth, hashtagListener.HashtagListener(time_limit=60))

hashtag = ''
try:
    hashtag = argv[1]
except IndexError as e:
    print('Please type a parameter for hashtag')

twitter_stream.filter(track=['' + hashtag + ''])
