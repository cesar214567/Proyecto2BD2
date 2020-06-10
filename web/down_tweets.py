import tweepy
import csv
import pandas as pd
from model import entities
from database import connector
from datetime import datetime


access_token = "104997748-7cCdw06UzvQI86C5bHskKl90qCPJi3vfbRTEef68"
access_token_secret = "ojBA7ZYhqrMrv6z0MqkonY74wOfQ9WZpNFloFgHykBib9"
consumer_key = "WKtmu8QRdyTtKDeMirpDW50zj"
consumer_secret = "G3pP3ZLJBcE7AHhiGAOsLPy06956oXUCbGstp0OIKM8EEH7312"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

db = connector.Manager()
engine = db.createEngine()


def get_tweets(busqueda,num):
    lista_tweets= []
    for tweet in tweepy.Cursor(api.search,q=busqueda,count=100,
                           lang="es",
                           since="2010-01-01").items(num):  
        if tweet.retweeted is not None:
            new_tweet = entities.Tweet( 
                        id = str(tweet.id),
                        text = tweet.text
                        ) 
            lista_tweets.append(new_tweet)            
    return lista_tweets

def get_tweet_by_id(id):
   
    tweet = api.get_status(id)
    return tweet


