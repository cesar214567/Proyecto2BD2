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

# Open/Create a file to append data
lista_tweets= []

db = connector.Manager()
engine = db.createEngine()

busqueda = input("Ingrese la busqueda: ")
for tweet in tweepy.Cursor(api.search,q=busqueda,count=100,
                           lang="en",
                           since="2019-01-01").items(10):  
     
    if tweet.retweeted is not None:
        new_tweet = entities.Tweet( 
                    id = str(tweet.id),
                    date = tweet.created_at, #datetime.strptime(str(tweet.created_at), '%y-%m-%d %H:%M:%S'),
                    text = tweet.text
                    ) 
        lista_tweets.append(new_tweet)   
        
session = db.getSession(engine)
for i in lista_tweets:
    session.add(i)
session.commit()


dbResponse = session.query(entities.Tweet)
for i in dbResponse:
    print(i.date)
    print("------------")
