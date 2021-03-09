import tweepy as tw
import numpy as np
import pandas as pd
import requests
import sys
import json
from datetime import datetime, timedelta

consumer_key = 'vbcxLowTDEJNYUzIecZmmQ'
consumer_secret = '1hUObCfVu6NP0dgIFBBMsk1kFNlR3xuslDA7hrer5s'
access_token = '13959882-Ruzo4TYImfPGKbsqyCOJmcwioJ9XuuA2i3AaVzm7T'
access_token_secret = 'DWe54s5cWbWGxTcM6XSEzLzBEmXMdqaHONA8WzYLDsKSu'
POLLUTION_API_URL = 'http://localhost:3000/report/'

if __name__ == "__main__":

    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True)

    # Define the search term and the date_since date as variables
    search_words = "#wildfires"
    date_since = "2018-11-16"

    # Collect tweets
    tweets = tw.Cursor(api.search,
              q=search_words,
              lang="en",
              since=date_since).items(20)

    # Iterate and print tweets
    for tweet in tweets:

#    tweets = [[tweet.id_str, tweet.user.screen_name, tweet.user.profile_image_url_https, 
#	tweet.text, "created_at": tweet.created_at, tweet.coordinates, tweet.place] for tweet in tweets]

        try:
          if json_object["geo"]["bbox"]!="null":
            address = tweet.place.fullname
            lat = tweet.place.geo.bbox[0]
            lng = tweet.place.geo.bbox[1]
        except:
          address = 'Ivano-Frankivsk'
          lat = 48.9183
          lng = 24.72

        data = {
           "orig_date":  datetime.strftime(tweet.created_at,'%Y-%m-%d %H:%M:%S'),
           "avatar": tweet.user.profile_image_url_https, 
           "description": tweet.text, 
           "address": address,
           "lat": lat,
           "lng": lng,
           "author": tweet.user.screen_name,
           "source": "Twitter",
           "id_str": tweet.id_str
        }
#        print(data)
#        print(tweet.coordinates)
        try:
          resp = requests.post(POLLUTION_API_URL, json=data)
          if resp.status_code != 201:
            raise ApiError('POST ' + POLLUTION_API_URL + ' {}'.format(resp.status_code))
          print('Created stats. ID: {}'.format(resp.json()["id"]))
        except:
          print ('Cant connect to API server')
          sys.exit()
