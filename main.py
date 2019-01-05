import config
import tweepy
from tweepy import OAuthHandler, Stream
import json
import hashtagListener

auth = OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_secret)

api = tweepy.API(auth)

twitter_stream = Stream(auth, hashtagListener.HashtagListener(time_limit=20))
twitter_stream.filter(track=['#governmentshutdown'])
