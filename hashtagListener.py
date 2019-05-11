from tweepy import Stream
from tweepy.streaming import StreamListener
import time

class HashtagListener(StreamListener):    
    def __init__(self, time_limit=60):
        self.start_time = time.time()
        self.limit = time_limit
        self.saveFile = open('file.json', 'a')
        super(HashtagListener, self).__init__()

    def on_connect(self):
        print("start fetching the tweets")

    def on_status(self, status):
        print(status.text)

    def on_data(self, data):
        if (time.time() - self.start_time) < self.limit:
            try:
                with open('file.json', 'a') as file:
                    file.write(data)
                    return True
            except BaseException as e:
                print("Error on_data: %s" % str(e))
        else:
            self.saveFile.close()
            print("it's time to close the stream")
            return False

    def on_error(self, status):
        print(status)
        return True

    def on_limit(self, track):
        print("limit is about to be reached ", track)

    def on_disconnect(self, notice):
        print("disconnected")
    
    def on_timeout(self):
        print("timeout")
