import tweepy
import random
import tkinter
from tweet import *
import classifier
import pandas as pd
import electionTester
from pprint import pprint
import twitconfig as cfg
consumer_key = cfg.twitter['consumer_key']
consumer_secret = cfg.twitter['consumer_secret']
access_token = cfg.twitter['access_token']
access_token_secret = cfg.twitter['access_token_secret']


class TwitWindow:
    def __init__(self, classifier, data='Live'):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)
        self.data = data
        if data == 'Live':
            self.public_tweets = self.api.home_timeline()
        elif data == 'Election':
            self.public_tweets = electionTester.parse_election()

        self.num_entries = len(self.public_tweets)
        # Lists to hold the labels and text areas
        self.texts = []
        self.labels = []
        self.classifier = classifier

    def CreateWindow(self):
        # Create the main window
        self.tkroot = tkinter.Tk()
        self.tkroot.title("Fake News Detector")
        # self.scrollbar = tkinter.Scrollbar(self.tkroot)
        # self.scrollbar.pack(side = RIGHT, fill = Y)
        # Create all the labels and text widgets:
        for i in range(0, self.num_entries):
            self.labels.append(tkinter.Label(self.tkroot))
            self.labels[i].pack(expand=False, fill=tkinter.X)

            self.texts.append(tkinter.Text())
            self.texts[i].config(width=55, height=3)
            self.texts[i].config(wrap=tkinter.WORD)
            self.texts[i].pack(expand=True)
            self.labels[i].config(bg="#07c", fg="white")
            self.texts[i].config(bg="#eff", fg="black")
        self.updateWindow()
        self.tkroot.mainloop()

    def updateWindow(self):
        statuses = self.public_tweets
        for i in range(0, self.num_entries):
            self.texts[i].delete(1.0, tkinter.END)  # Clear the old text

            if i < len(statuses):
                # Update the label with the user's name and screen name
                user = statuses[i].user
                if self.data == 'Live':
                    labeltext = user.name + " (" + user.screen_name + ")"
                else:
                    labeltext = 'anonymous user'
                self.labels[i].config(text=labeltext)

                # Display the text of the tweet
                if self.data == 'Live':
                    tweetJSON = vars(statuses[i])['_json']
                    tweet = Tweet()
                    tweet.phemeTweet(tweetJSON)
                else:
                    tweet = statuses[i]
                prediction, probability = self.classifier.predict(tweet)
                if prediction == 0:
                    self.labels[i].config(bg="red")
                if prediction == 1:
                    self.labels[i].config(bg="green")
                if prediction == 2:
                    self.labels[i].config(bg='yellow')
                print(statuses[i].text)
                print('Prediction: ' + str(prediction))
                print('Probability: ' + str(probability))
                self.texts[i].insert(tkinter.END, statuses[i].text)
