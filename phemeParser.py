#for parsing the PHEME repositiory
import json
import os
import pandas as pd
from pandas.io.json import json_normalize
from itertools import chain
### USER VARIABLES ###
#Link to PHEME dataset: https://figshare.com/articles/PHEME_rumour_scheme_dataset_journalism_use_case/2068650 #

### Replace with location of PHEME dataset. Should be something like C:\...Documents\PHEME ###
pathToPheme = 'C:\\Users\\EECS\\Documents'

class Tweet:
    def __init__(self, text, favCount, retCount, id, isReply, user):
        self.tweet_text=text
        self.favorite_count = favCount
        self.retCount = retCount
        self.user = user
        self.id = id
        self.isReply = isReply
        self.replyList = None
        self.annotation = None

    def __str__(self):
        return self.tweet_text + ' - ' + self.user.name

    def to_dict(self):
        return {
            'tweet_text' : self.tweet_text,
            'favorite_count' : self.favorite_count,
            'ret_count' : self.retCount,
            'user' : self.user,
            'tweetid' : self.id,
            'reply' : self.isReply,
            'annotation' : self.annotation,
            'replyList' : self.replyList
        }

class User:
    def __init__(self, name, screenName, favorite_count, follower_count, description, verified, friends_count):
        self.name = name
        self.screenName = screenName
        self.favorite_count = favorite_count
        self.follower_count = follower_count
        self.description = description
        self.verified = verified
        self.friends_count = friends_count

''' returns annotations for each tweet '''
def loadAnnotations(path):
    annotationFile = path + '\\PHEME\\pheme-rumour-scheme-dataset\\annotations\\en-scheme-annotations.json'
    with open(annotationFile) as f:
        data = []
        for line in f:
            if not '#' in line:
                data.append(json.loads(line))
        return pd.DataFrame(data)

''' crawls PHEME directory and processes tweets, replies, and annotations'''
def crawlDirectory(path, annotations):
    path += '\\PHEME\\pheme-rumour-scheme-dataset\\threads\\en'
    #temp = [processCategory(path + '\\' + dirName, annotations) for dirName in os.listdir(path)]
    #temp = list(chain.from_iterable([processCategory(path + '\\' + dirName, annotations) for dirName in os.listdir(path)]))

    allThreads = []
    allTweets = []
    for threads, tweets in [processCategory(path + '\\' + dirName, annotations) for dirName in os.listdir(path)]:
        allThreads += threads
        allTweets += tweets
    return threads, allTweets

def processCategory(path, annotations):
    ''' processes each tweet topic
    output: List[thread, allTweets]
    '''
    threads = []
    allTweets = []
    for thread, tweets in [processTweetFolder(path + '\\' + tweetFolder, tweetFolder, annotations) for tweetFolder in os.listdir(path)]:
        threads.append(thread)
        allTweets += tweets
    return threads, allTweets

def processTweetFolder(path, tweetNumber, annotations):
    ''' processes each tweet thread
    output: single tweet (Source of thread, all tweets in the thread)
    '''

    thread = processTweetJSON(path+'\\source-tweets\\' + tweetNumber + '.json', False, annotations)
    allTweets = [thread]
    replyList = [processTweetJSON(path + '\\reactions\\' + tweetJSON, True, annotations) for tweetJSON in os.listdir(path + '\\reactions')]
    allTweets += replyList
    thread.replyList = replyList
    return thread, allTweets

'''processes the individual tweet JSON'''
def processTweetJSON(path, isReply, annotations):
    with open(path) as f:
        data = json.load(f)
        userData = data['user']
        user = User(userData['name'], userData['screen_name'], userData['favourites_count'], userData['followers_count'], userData['description'], userData['verified'], userData['friends_count'])
        tweet = Tweet(data['text'], data['favorite_count'], data['retweet_count'], data['id_str'], isReply, user)
        tweet.annotation = annotations[annotations['tweetid'] == tweet.id].to_dict('r') #keeps dataframe id out of the mix
        return tweet

''' parses the entire PHEME dataset (main function) '''
def parsePheme(pathToPheme):
    return crawlDirectory(pathToPheme, loadAnnotations(pathToPheme))
