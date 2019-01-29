import json
import os
import pandas as pd
from pandas.io.json import json_normalize
from itertools import chain
from tweet import *
from anytree import Node, RenderTree

### USER VARIABLES ###
#Link to PHEME dataset: https://figshare.com/articles/PHEME_rumour_scheme_dataset_journalism_use_case/2068650 #

### Replace with location of PHEME dataset. Should be something like C:\...Documents\PHEME ###
pathToPheme = 'C:\\Users\\EECS\\Documents'


def loadAnnotations(path):
    """Returns annotation dataframe for all tweets in PHEME dataset

    Keyword arguments:
    path -- path to the location of the PHEME dataset
    """

    annotationFile = path + '\\PHEME\\pheme-rumour-scheme-dataset\\annotations\\en-scheme-annotations.json'
    with open(annotationFile) as f:
        return pd.DataFrame([json.loads(line) for line in f if not '#' in line])

def crawlDirectory(path, annotations):
    """crawls PHEME directory and returns list of all conversation threads

    Keyword arguments:
    path -- path to directory
    annotations -- dataframe of all annotations
    """
    path += '\\PHEME\\pheme-rumour-scheme-dataset\\threads\\en'
    allThreads, allTweets = [], []

    for threads, tweets in [processCategory(path + '\\' + dirName, annotations) for dirName in os.listdir(path)]:
        allThreads += threads
        allTweets += tweets

    return threads, allTweets

def processCategory(path, annotations):
    """Processes a PHEME tweet topic

    Keyword arguments:
    path -- path to the topics
    annotations -- dataframe of all annotations
    """
    threads = []
    allTweets = []
    for thread, tweets in [processTweetFolder(path + '\\' + tweetFolder, tweetFolder, annotations) for tweetFolder in os.listdir(path)]:
        threads.append(thread)
        allTweets += tweets
    return threads, allTweets

def processTweetFolder(path, tweetid, annotations):
    """Processes an entire thread and returns a tweet with all replies


    Keyword arguments:
    path -- path to threads
    tweetid -- tweetid of thread
    annotations -- dataframe of all annotations
    """
    thread = processTweetJSON(path+'\\source-tweets\\' + tweetid + '.json', False, annotations)
    with open(path +  '\\annotation.json') as f:
        thread.threadAnnotation = json.load(f)
    allTweets = [thread]
    replyList = [processTweetJSON(path + '\\reactions\\' + tweetJSON, True, annotations) for tweetJSON in os.listdir(path + '\\reactions')]
    replyChain = processReplies(path, tweetid, annotations, thread)
    allTweets += replyList
    thread.replyList = replyList
    return thread, allTweets

def processReplies(path, tweetid, annotations, root):
    """Creates a tree structure out of replies

    Keyword arguments:
    path -- path to JSON
    is_reply -- boolean denoting whether tweet is a reply
    annotations -- dataframe of all annotations
    """
    structure = None
    with open(path + '\\structure.json') as f:
        structure = json.load(f)
    root = Node(str(tweetid), tweet=root)
    processTree(structure[tweetid], root, path + '\\reactions\\', annotations)
    #for pre, _, node in RenderTree(root):
    #    print('-'*len(pre) + node.name)
    return root

def processTree(children, parent, path, annotations):
    """Returns tree of replies

    Keyword arguments:
    children -- dictionary of children remaining
    parent -- Node of parent
    """
    if not children:
        return
    for key, value in children.items():
        temp = Node(key, parent=parent, tweet=processTweetJSON(path + key + '.json', True, annotations))
        processTree(value, temp, path, annotations)

def processTweetJSON(path, is_reply, annotations):
    """Processes and returns an individual tweet JSON

    Keyword arguments:
    path -- path to JSON
    is_reply -- boolean denoting whether tweet is a reply
    annotations -- dataframe of all annotations
    """

    with open(path) as f:
        data = json.load(f)
        userData = data['user']
        user = User()
        tweet = Tweet()
        user.phemeUser(userData['name'], userData['screen_name'], userData['favourites_count'], userData['followers_count'], userData['description'], userData['verified'], userData['friends_count'])
        tweet.phemeTweet(data['text'], data['favorite_count'], data['retweet_count'], data['id_str'], is_reply, user)
        tweet.annotation = annotations[annotations['tweetid'] == tweet.tweetid].to_dict('r') #keeps dataframe id out of the mix
        return tweet

def parsePheme(pathToPheme):
    """Parses PHEME dataset and returns a list of all conversation threads

    Keyword arguments:
    pathToPheme -- path to PHEME dataset
    """
    return crawlDirectory(pathToPheme, loadAnnotations(pathToPheme))
parsePheme(pathToPheme)
