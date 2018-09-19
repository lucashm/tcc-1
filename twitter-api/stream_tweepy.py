from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import api
import time
import json
import csv

with open('twitter_credentials.json', 'r') as file:
    creds = json.load(file)

auth = OAuthHandler(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])
auth.set_access_token(creds['ACCESS_TOKEN'], creds['ACCESS_KEY'])

csv_file = open('bolsonaro.csv', 'a')
csv_writer = csv.writer(csv_file)

def remove_special_characters(line):
    for char in '[\n\'\"]':
        line = line.replace(char, '')
    
    return line


class MyStreamListener(StreamListener):

    def __init__(self, time_limit=5):
        self.start_time = time.time()
        self.limit = time_limit
        super(MyStreamListener, self).__init__()

    def on_status(self, status):
        # print(status.text)
        if hasattr(status, 'extended_tweet'):
            # print('caso 1')
            line = remove_special_characters(str(status.extended_tweet['full_text']))
            print(line)
            
            csv_writer.writerow([line])

        elif hasattr(status, 'retweeted_status'):
            if hasattr(status.retweeted_status, 'extended_tweet'):
                # print('caso 2')
                line = remove_special_characters(str(status.retweeted_status.extended_tweet['full_text']))
                print(line)
                csv_writer.writerow([line])
            else:
                # print('caso 3')
                line = remove_special_characters(status.retweeted_status.text)
                print(line)
                csv_writer.writerow([line])
        else:
            # print('caso 4')
            line = remove_special_characters(status.text)
            print(line)
            csv_writer.writerow([line])

    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False


myStreamListener = MyStreamListener()
myStream = Stream(auth, myStreamListener, tweet_mode= 'extended')

init = time.time()
limit = 10

# while time.time() - init < limit:
while True:
    try:
        myStream.filter(track=['bolsonaro'])
    except:
        continue