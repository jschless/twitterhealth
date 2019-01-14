#for parsing the PHEME repositiory
import json
import os

annotationFile = 'C:\\Users\\EECS\\Documents\\PHEME\\pheme-rumour-scheme-dataset\\annoations\\en-scheme-annotations.json'

tweetList = []
#annotationJSON = json.read(annotationFile)

class Tweet:
    def __init__(self, text, favCount, retCount, user):
        self.tweet_text=text
        self.favorite_count = favCount
        self.retCount = retCount
        self.user = user

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
    processTweetJSON(dirName+'\\source-tweets\\' + tweetNumber + '.json')
    for tweetJSON in os.listdir(dirName + '\\reactions'):
        processTweetJSON(dirName + '\\reactions\\' + tweetJSON)

def processTweetJSON(path):
    with open(path) as f:
        data = json.load(f)
        userData = data['user']
        user = User(userData['name'], userData['screen_name'], userData['favourites_count'], userData['followers_count'], userData['description'], userData['verified'], userData['friends_count'])
        tweet = Tweet(data['text'], data['favorite_count'], data['retweet_count'], user)
        tweetList.append(tweet)

crawlDirectory('C:\\Users\\EECS\\Documents\\PHEME\\pheme-rumour-scheme-dataset\\threads\\en')
#crawlDirectory()
#processTweetJSON('C:\\Users\\EECS\\Documents\\PHEME\\pheme-rumour-scheme-dataset\\threads\\en\\charliehebdo\\552783667052167168\\source-tweets\\552783667052167168.json')
