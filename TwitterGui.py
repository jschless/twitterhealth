import tweepy
import tkinter
from tweet import *
import classifier
import pandas as pd
from pprint import pprint
consumer_key = 'L6JvqYzvUeHX36sYTR8O3E7gD'
consumer_secret = 'VKVPjkonSRUBzOsaiNKdcFToDISJ0ga3vGGvNuDo6nAfRtABU1'
access_token = '1052184206368002049-9RSvx4QK9Js4gnMrMY8GCMvQYYPtPJ'
access_token_secret = 'KUykgZdc8vIzDph3CasS91i7foWks8Y6NtLTpBxPTl3BR'

class TwitWindow :
    def __init__(self) :
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)
        self.public_tweets = self.api.home_timeline()
        self.num_entries = len(self.public_tweets)
        # Lists to hold the labels and text areas
        self.labels = []
        self.texts = []
        self.classifier = classifier.main()
        print(self.classifier)

    def CreateWindow(self):
        # Create the main window
        self.tkroot = tkinter.Tk()
        self.tkroot.title("Fake News Detector")
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
        statuses = self.api.home_timeline()
        for i in range(0, self.num_entries):
            self.texts[i].delete(1.0, tkinter.END)  # Clear the old text

            if i < len(statuses):
                # Update the label with the user's name and screen name
                user = statuses[i].user
                labeltext = user.name + " (" + user.screen_name + ")"
                self.labels[i].config(text=labeltext)

                # Display the text of the tweet
                tweetJSON = vars(statuses[i])['_json']
                #pprint(tweetJSON)
                tweet = Tweet()
                tweet.phemeTweet(tweetJSON)
                prediction = classifier.predict(tweet, self.classifier)
                print(statuses[i].text)
                print(prediction)
                self.texts[i].insert(tkinter.END, statuses[i].text)


win = TwitWindow()
win.CreateWindow()
