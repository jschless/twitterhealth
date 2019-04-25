import pandas as pd
import twitconfig as cfg
from tweet import *
path = cfg.election_interference_path

n_tweets = 10000

# datasets must come from Twitter
# https://about.twitter.com/en_us/values/elections-integrity.html#data
datasets = [
    ("ira_tweets_csv_hashed.csv", "ira_users_csv_hashed")
    # ("iranian_tweets_csv_hashed.csv", "iranian_users_csv_hashed")
]


def load_data():
    tweets = pd.concat(
        [pd.read_csv(path + '\\' + tweets, nrows=n_tweets, encoding='utf-8')
            for tweets, users in datasets]
    )
    users = pd.concat(
        [pd.read_csv(path + '\\' + users, encoding='utf-8')
            for tweets, users in datasets]
    )

    return tweets, users


def parse_election():
    tweets, users = load_data()
    tweets = tweets[tweets['tweet_language'] == 'en']
    tweet_list = tweets.to_dict(orient='records')
    return_list = []
    for dict in tweet_list:
        tweet = Tweet()
        tweet.csvTweet(dict)
        user = User()
        temp = users.loc[users['userid'] == tweet.userid]
        temp = temp.to_dict(orient='records')[0]
        user.csvUser(temp)
        tweet.user = user
        return_list.append(tweet)
    return return_list
