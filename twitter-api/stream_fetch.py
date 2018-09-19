from twython import TwythonStreamer
import json
import csv
import pandas as pd
import time

with open('twitter_credentials.json', 'r') as file:
    creds = json.load(file)

# Filter out unwanted data
def process_tweet(tweet):  
    d = {}
    d['hashtags'] = [hashtag['text'] for hashtag in tweet['entities']['hashtags']]
    d['text'] = tweet['text']
    d['user'] = tweet['user']['screen_name']
    d['user_loc'] = tweet['user']['location']
    return d

class MyStreamer(TwythonStreamer):
    def on_success(self, data):
        # if data['lang'] == 'pt':
        if 'text' in data:
            print(data['text'])
            # tweet_data = process_tweet(data)
            # self.save_to_csv(tweet_data)

    def on_error(self, status_code, data):
        print(status_code)
        # self.disconnect()

    def save_to_csv(self, tweet):
        with open(r'saved_tweets.csv', 'a') as file:
            writer = csv.writer(file)
            writer.writerow(list(tweet.values()))


# Instantiate from our streaming class
stream = MyStreamer(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'],  
                    creds['ACCESS_TOKEN'], creds['ACCESS_KEY'], retry_in=1)
# Start the stream
stream.statuses.filter(track='evangelion', async=True)

