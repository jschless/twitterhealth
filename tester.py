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
    tweetList.append(Tweet(data.iloc[row]))
