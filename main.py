import config
import sys
import tweepy
from tweepy import OAuthHandler, Stream
import json
import hashtagListener

auth = OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_secret)

api = tweepy.API(auth)

twitter_stream = Stream(auth, hashtagListener.HashtagListener(time_limit=60))

hashtag = ''
try:
    hashtag = sys.argv[1]
except IndexError as e:
    print('Please type a parameter for hashtag')

twitter_stream.filter(track=['#' + sys.argv[1] + ''])
