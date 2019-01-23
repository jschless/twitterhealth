'''
Tests our model on new data.
'''
import pandas as pd
import classifier
import phemeParser
from tweet import *
data = pd.read_csv('small.csv')

tweetList = []
for row in range(len(data)):
    tweet = Tweet()
    tweet.dfTweet(data.iloc[row])
    tweetList.append(tweet)

classifier.main(tweetList)
