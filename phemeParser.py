#for parsing the PHEME repositiory
import json
import os
import pandas as pd
from pandas.io.json import json_normalize

annotationFile = 'C:\\Users\\EECS\\Documents\\PHEME\\pheme-rumour-scheme-dataset\\annotations\\en-scheme-annotations.json'
annotationDF = None
with open(annotationFile) as f:
    data = []
    for line in f:
        if not '#' in line:
            data.append(json.loads(line))
    annotationDF = pd.DataFrame(data)

threadList = []

class Tweet:
    def __init__(self, text, favCount, retCount, id, isReply, user):
        self.tweet_text=text
        self.favorite_count = favCount
        self.retCount = retCount
        self.user = user
        self.id = id
        self.annotation = annotationDF[annotationDF['tweetid'] == self.id].to_dict()
        self.isReply = True

    def __str__(self):
        return self.tweet_text + ' - ' + self.user.name

class User:
    def __init__(self, name, screenName, favorite_count, follower_count, description, verified, friends_count):
        self.name = name
        self.screenName = screenName
        self.favorite_count = favorite_count
        self.follower_count = follower_count
        self.description = description
        self.verified = verified
        self.friends_count = friends_count

def crawlDirectory(rootDir):
    for dirName in os.listdir(rootDir):
        processCategory(rootDir + '\\' + dirName)

def processCategory(dirName):
    for tweetFolder in os.listdir(dirName):
        processTweetFolder(dirName + '\\' + tweetFolder, tweetFolder)

def processTweetFolder(dirName, tweetNumber):
    tweet = processTweetJSON(dirName+'\\source-tweets\\' + tweetNumber + '.json', False)
    replyList = [processTweetJSON(dirName + '\\reactions\\' + tweetJSON, True) for tweetJSON in os.listdir(dirName + '\\reactions')]
    threadList.append(tweet)

def processAnnotationJSON(path):
    with open(path) as f:
        return json.load(f)

def processTweetJSON(path, isReply):
    with open(path) as f:
        data = json.load(f)
        userData = data['user']
        user = User(userData['name'], userData['screen_name'], userData['favourites_count'], userData['followers_count'], userData['description'], userData['verified'], userData['friends_count'])
        tweet = Tweet(data['text'], data['favorite_count'], data['retweet_count'], data['id_str'], isReply, user)
        tweet.replyList = None
        return tweet

crawlDirectory('C:\\Users\\EECS\\Documents\\PHEME\\pheme-rumour-scheme-dataset\\threads\\en')
