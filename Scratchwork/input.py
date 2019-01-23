import numpy as np
import pandas as pd

class Tweet:
    def __str__(self):
        return self.tweet_text + " - " + self.user.user_screen_name

class User:
    def __str__(self):
        return self.user_display_name

testUser = User()
testUser.user_display_name = 'Big pimpin'
testUser.user_screen_name = 'grit'
testUser.follower_count = 130000
testUser.following_count = 400

testTweet = Tweet()
testTweet.user = testUser
testTweet.tweet_text = 'this is a tweet, analyze it'
testTweet.quote_count = 20
testTweet.reply_count = 40
testTweet.like_count = 4500
testTweet.retweet_count = 32222
testTweet.hashtags = ['winning', 'trump', 'newyearnewme']


print(testUser.follower_count)
