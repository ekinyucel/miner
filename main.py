import config
from sys import argv
import tweepy as tw
from tweepy import OAuthHandler, Stream
from kafka.client import KafkaClient
from kafka.producer import KafkaProducer
from kafka import KafkaConsumer
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

    api = tw.API(auth)

    #client = KafkaClient("localhost:9092")
    producer = KafkaProducer(bootstrap_servers='localhost:9092')

    streamListener = tweetListener.TweetListener(kafkaProducer=producer, time_limit=5400)
    twitter_stream = tw.Stream(auth=api.auth, listener=streamListener)

    twitter_stream.filter(track=queries)

start_mining(['' + searchText + ''])