import config
from sys import argv
import tweepy
from tweepy import OAuthHandler, Stream
import json
import tweetListener

searchText = ''
try:
    searchText = argv[1]
except IndexError as e:
    print('Please type a parameter to searchs')

def start_mining(queries):
    # create your own config.py file then define your own twitter API credentials
    auth = OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token, config.access_secret)

    api = tweepy.API(auth)

    streamListener = tweetListener.TweetListener(time_limit=60)
    twitter_stream = tweepy.Stream(auth=api.auth, listener=streamListener)

    twitter_stream.filter(track=queries, )

start_mining(['' + searchText + ''])
