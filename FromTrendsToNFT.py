from logging import exception
import os
import tweepy

#Retreive keys and tokens
path = 'auth.txt'
lines = []
with open(path,"r") as f:
    lines =  f.readlines()
       
consumer_key = lines[0][8:]
consumer_secret = lines[1][14:]
access_token = lines[2][12:]
access_token_secret = lines[3][18:]


#set up authentification
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

#initiate api object
api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("Everythin works")
except Exception as e:
    print(e)

# #test to retreive tweets from the timeline/feed?
# public_tweets = api.home_timeline()
# for tweet in public_tweets:
#     print(tweet.text)