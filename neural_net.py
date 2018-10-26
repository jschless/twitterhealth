from keras.models import Sequential
from keras.layers import Dense, Activation
import numpy as np
import pandas as pd
import re
from textblob import TextBlob

df = pd.read_csv('C:\\Users\\x92423\\Downloads\\iranian_tweets_csv_hashed\\small.csv')


### pick columns of interest from dataset ###

dataset = df[['follower_count', 'following_count', 'like_count', 'retweet_count']]
dataset_size = len(df['tweet_text'])

### quantify text sentiment ###
for i in range(dataset_size):
    tweet = df.loc[df.index[i], 'tweet_text']
    clean_tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
    analysis = TextBlob(clean_tweet)
    dataset.loc[dataset.index[i],'tweet_text'] = analysis.sentiment.polarity
    
model = Sequential()
model.add(Dense(8, input_dim=5, activation='relu'))
model.add(Dense(1, activation='sigmoid'))
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

#set X and Y for neural network
X = dataset

#Y is randomly 0 or 1 right now because
#all of these tweets are election interference
Y = [0 if x%2==0 else 1 for x in range(dataset_size)]
model.fit(X,Y, epochs=150)
scores = model.evaluate(X,Y)

print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

print(X.head())
