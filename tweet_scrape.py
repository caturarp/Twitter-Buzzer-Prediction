# Import and Install Dependencies
import snscrape.modules.twitter as sntwitter
import pandas as pd
import numpy as np
import re
import tweepy
import twitter
import time
from datetime import datetime, timedelta
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initialize Analyzer
sid = SentimentIntensityAnalyzer()

# define credentials
consumer_key = "2CW39gBbl8RaL6ED9lUGUL3Kt"
consumer_secret = "TiaGBqh9qUqL3Dx1bV9abI3jfMeuXfXa7Ko0xKWoioOn0DhOPm"
access_token = "1520536260300787712-Rtwy55jn2E7HvQCqKqywDlF20QMXfg"
access_token_secret = "kK8p1RFbH3WnYo1eFuTCIdIggypIrQrIIj2PXaVTaBW18"

# create instance twitter with credentials
api = twitter.Api(consumer_key= "2CW39gBbl8RaL6ED9lUGUL3Kt",
                  consumer_secret="TiaGBqh9qUqL3Dx1bV9abI3jfMeuXfXa7Ko0xKWoioOn0DhOPm",
                  access_token_key="1520536260300787712-Rtwy55jn2E7HvQCqKqywDlF20QMXfg",
                  access_token_secret="kK8p1RFbH3WnYo1eFuTCIdIggypIrQrIIj2PXaVTaBW18",
                  sleep_on_rate_limit=True)

def scrape_tweets(username):
    tweets_list = []
    compound_scores = []  
    #authenticating the developer account 
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    tweets = tweepy.Cursor(api.search,q='from:'+username, tweet_mode='extended').items(10)
    for tweet in tweets:
        try:
            content = re.sub(r'[^\x00-\x7f]', r'', tweet.full_text) # remove non-ascii characters (emoji)
            content = re.sub(r'@\w+', r'', content) # remove mentions ex. @namaakun    
            tweets_list.append([content])
            # analyze the sentiment of the tweet
            scores = sid.polarity_scores(content)
            compound_scores.append(scores["compound"]) # get the compound score
        except UnicodeEncodeError:
            continue
    if len(compound_scores) == 0:
        compound_mean = 0
        return compound_mean
    # calculate the mean of the up to 10 compound score
    compound_mean = sum(compound_scores) / len(compound_scores)
    return compound_mean
# def scrape_tweets(username):
#     tweets_list = []
#     compound_scores = []    
#     # scrape until
#     for i,tweet in enumerate(sntwitter.TwitterSearchScraper('from:'+username).get_items()):
#         if i>10: # limit the number of tweets to 10
#             break
#         print(tweet)
#         try:
#             content = re.sub(r'[^\x00-\x7f]', r'', tweet.content) # remove non-ascii characters (emoji)
#             content = re.sub(r'@\w+', r'', content) # remove mentions ex. @namaakun    
#             tweets_list.append([content])
#             # analyze the sentiment of the tweet
#             scores = sid.polarity_scores(content)
#             compound_scores.append(scores["compound"]) # get the compound score
#         except UnicodeEncodeError:
#             continue
#     # calculate the mean of the up to 10 compound score
#     compound_mean = sum(compound_scores) / len(compound_scores)
#     return compound_mean

# # example usage
# mean_score = scrape_tweets("caturaperkasa")
# print(mean_score)

def get_account_info(username):
    # Creating list to append account age data to
    infos_list = []
    try:
        # Fetch the user's account creation date
        account_created = api.GetUser(screen_name=username).created_at
        # Get Age
        account_created = int(account_created.split(" ")[-1])
        account_created = 2022 - account_created
        # Fetch the user's friends and followers
        friends = api.GetUser(screen_name=username).friends_count
        followers = api.GetUser(screen_name=username).followers_count
        # Append to list of dictionaries
        infos_list.append({"account_age": account_created, "following": friends, "followers": followers})
        print(username + ' success')
        return infos_list

    except Exception as e:
        # If an error occurs, print a message and move on to the next username
        print(f'An error occurred for {username}')
        infos_list.append({"username": username, "account_age": "failed"})
        
        print(username + ' failed')

        return infos_list


def get_account_info_and_scrape_tweets(username):
    infos_list = get_account_info(username)
    compound_mean = scrape_tweets(username)
    infos_list[0]["compound_mean"] = compound_mean
    return infos_list