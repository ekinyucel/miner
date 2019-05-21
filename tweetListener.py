from tweepy import Stream
from tweepy.streaming import StreamListener
from kafka import KafkaProducer
import time
import csv

class TweetListener(StreamListener):
    def __init__(self, kafkaProducer, time_limit=60):
        self.start_time = time.time()
        self.limit = time_limit
        self.producer = kafkaProducer
        self.filename = 'data'+'_'+time.strftime('%Y%m%d-%H%M%S')+'.csv'
        csvfile = open(self.filename, 'w')

        csvWriter = csv.writer(csvfile, delimiter=";", quoting=csv.QUOTE_ALL)

        csvWriter.writerow(['text',
                            'created_at',
                            'geo',
                            'lang',
                            'place',
                            'coordinates',
                            'user.favourites_count',
                            'user.statuses_count',
                            'user.description',
                            'user.location',
                            'user.id',
                            'user.created_at',
                            'user.verified',
                            'user.following',
                            'user.url',
                            'user.listed_count',
                            'user.followers_count',
                            'user.default_profile_image',
                            'user.utc_offset',
                            'user.friends_count',
                            'user.default_profile',
                            'user.name',
                            'user.lang',
                            'user.screen_name',
                            'user.geo_enabled',
                            'user.profile_image_url',
                            'user.time_zone',
                            'id',
                            'favorite_count',
                            'retweeted',
                            'source',
                            'favorited',
                            'retweet_count'])

        super(TweetListener, self).__init__()

    def clean_data(self, input):
        return input.replace("\n", "")

    def on_connect(self):
        print("start fetching the tweets")

    def on_status(self, status):
        if (time.time() - self.start_time) < self.limit:
            csvFile = open(self.filename, 'a', newline = '', encoding='utf-8')
            csvWriter = csv.writer(csvFile, delimiter=";", quoting=csv.QUOTE_ALL)
            if not 'RT @' in status.text:
                try:
                    status_text = self.clean_data(status.text)
                    user_description = self.clean_data(status.user.description)
                    csvWriter.writerow([status_text,
                                        status.created_at,
                                        status.geo,
                                        status.lang,
                                        status.place,
                                        status.coordinates,
                                        status.user.favourites_count,
                                        status.user.statuses_count,
                                        user_description,
                                        status.user.location,
                                        status.user.id,
                                        status.user.created_at,
                                        status.user.verified,
                                        status.user.following,
                                        status.user.url,
                                        status.user.listed_count,
                                        status.user.followers_count,
                                        status.user.default_profile_image,
                                        status.user.utc_offset,
                                        status.user.friends_count,
                                        status.user.default_profile,
                                        status.user.name,
                                        status.user.lang,
                                        status.user.screen_name,
                                        status.user.geo_enabled,
                                        status.user.profile_image_url,
                                        status.user.time_zone,
                                        status.id,
                                        status.favorite_count,
                                        status.retweeted,
                                        status.source,
                                        status.favorited,
                                        status.retweet_count])                    
                    message = status.text + ',' + status.user.screen_name
                    # sending tweets to kafka broker
                    producer.send('tweet', str(message))
                except BaseException as e:
                    print("Error on_data: %s" % str(e))
                csvFile.close()
                return
        else:
            print("it's time to close the stream")
            return False

    def on_error(self, status):
        if status == 420:
            return False
        elif status == 401:
            print("authorization required")

        print("error ", status)
        return True

    def on_limit(self, track):
        print("limit is about to be reached ", track)
        return True

    def on_disconnect(self, notice):
        print("disconnected")

    def on_delete(self, status_id, user_id):
        return

    def on_timeout(self):
        print("timeout")
        return
