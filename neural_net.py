from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.utils import plot_model
import numpy as np
import pandas as pd
import re
from textblob import TextBlob

df = pd.read_csv('C:\\Users\\x92423\\Downloads\\iranian_tweets_csv_hashed\\small.csv')


#pick columns of interest from dataset

#turn text into sentiment

dataset = df[['follower_count', 'following_count', 'like_count', 'retweet_count']]
tweet_text = df['tweet_text']
dataset_size = len(df['tweet_text'])
for i in range(dataset_size):
    tweet = df.at[df.index[i], 'tweet_text']
    clean_tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
    analysis = TextBlob(clean_tweet)
    dataset.at[dataset.index[i],'tweet_text'] = analysis.sentiment.polarity


    
model = Sequential()
model.add(Dense(8, input_dim=5, activation='relu'))
model.add(Dense(1, activation='sigmoid'))
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

print(dataset)

X = dataset
Y = [0 if x%2==0 else 1 for x in range(dataset_size)]
model.fit(X,Y, epochs=150)
scores = model.evaluate(X,Y)

print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
