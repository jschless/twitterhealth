import numpy as np
import pandas as pd

def processDataSet(path):
    tweets = {}
    users = {}
    df = pd.read_csv(path)
    for row in range(len(df)):
        tweet = Tweet(df.iloc[row])        
        tweets[tweet.tweetid] = tweet
        users[tweet.userid] = tweet.user

    for tweetid, tweet in tweets.items():
        print(str(tweet))
        
class Tweet:
    def __init__(self, dataframe):
        self.tweetid = dataframe['tweetid']
        self.userid = dataframe['userid']
        self.user = User(dataframe)
        self.tweet_language = dataframe['tweet_language']
        self.tweet_text = dataframe['tweet_text']
        self.tweet_time = dataframe['tweet_time']
        self.in_reply_to_userid = dataframe['in_reply_to_userid']
        self.in_reply_to_tweetid = dataframe['in_reply_to_tweetid']
        self.quoted_tweet_tweetid = dataframe['quoted_tweet_tweetid']
        self.is_retweet = dataframe['is_retweet']
        self.retweet_userid = dataframe['retweet_userid']
        self.retweet_tweetid = dataframe['retweet_tweetid']
        self.latitude = dataframe['latitude']
        self.longitude = dataframe['longitude']
        self.quote_count = dataframe['quote_count']
        self.reply_count = dataframe['reply_count']
        self.like_count = dataframe['like_count']
        self.retweet_count = dataframe['retweet_count']
        self.hashtags = dataframe['hashtags']
        self.urls = dataframe['urls']
        self.user_mentions = dataframe['user_mentions']

    def __str__(self):
        return self.tweet_text + " - " + self.user.user_screen_name

class User:
    def __init__(self, dataframe):
        self.userid= dataframe['userid']
        self.user_display_name = dataframe['user_display_name']
        self.user_screen_name = dataframe['user_screen_name']
        self.user_reported_location = dataframe['user_reported_location']
        self.user_profile_description = dataframe['user_profile_description']
        self.user_profile_url = dataframe['user_profile_url']
        self.follower_count = dataframe['follower_count']
        self.following_count = dataframe['following_count']
        self.account_creation_date = dataframe['account_creation_date']
        self.account_language = dataframe['account_language']

    def __str__(self):
        return self.user_display_name

processDataSet('small.csv')
