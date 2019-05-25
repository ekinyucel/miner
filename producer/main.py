import config
from sys import argv
import tweepy as tw
from tweepy import OAuthHandler, Stream
from kafka import KafkaConsumer, KafkaProducer
import json
import tweetListener

searchText = ''
try:
    searchText = argv[1]
except IndexError as e:
    print('Please type a parameter to searchs')

def connect_kafka_producer():
    _producer = None
    try:
        _producer = KafkaProducer(bootstrap_servers=[config.kafka_server], api_version=(0, 10))
    except Exception as ex:
        print('Exception while connecting Kafka')
        print(str(ex))
    finally:
        print('Successfully connected to Kafka broker')
        return _producer

def start_mining(queries):
    # create your own config.py file then define your own twitter API credentials
    auth = OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token, config.access_secret)

    api = tw.API(auth)
    
    producer = connect_kafka_producer()

    streamListener = tweetListener.TweetListener(kafkaProducer=producer, query=queries, time_limit=540)
    twitter_stream = tw.Stream(auth=api.auth, listener=streamListener)

    twitter_stream.filter(track=queries)

start_mining(['' + searchText + ''])

consumer = KafkaConsumer('tweet', bootstrap_servers=[config.kafka_server])

for msg in consumer:
    print(msg.value)

consumer.close()