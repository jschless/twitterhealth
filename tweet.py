from collections import namedtuple
import json
class Tweet(object):
    def __init__(self):
        self.reply_list = None
        self.annotation = None
        self.thread_annotation = None

    def phemeTweet(self, dict):
        for key, value in dict.items():
            setattr(self, key, value)
            if key == 'user':
                user = User()
                user.phemeUser(value)
                self.user = user

    def dfTweet(self, dataframe):
        self.tweetid = dataframe['tweetid']
        self.userid = dataframe['userid']
        self.user = User()
        self.user.dfUser(dataframe)
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
        self.favorite_count = dataframe['like_count']
        self.retweet_count = dataframe['retweet_count']
        self.hashtags = dataframe['hashtags']
        self.urls = dataframe['urls']
        self.user_mentions = dataframe['user_mentions']
        self.is_reply = (self.in_reply_to_userid is not None)

    def __str__(self):
        return self.text + ' - ' + self.screen_name

class User:
    def phemeUser(self, dict):
        for key, value in dict.items():
            setattr(self, key, value)
