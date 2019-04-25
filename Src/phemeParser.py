import json
import os
import pandas as pd
from pandas.io.json import json_normalize
from itertools import chain
from tweet import *
from anytree import Node, RenderTree, DoubleStyle, AsciiStyle
from pprint import pprint
import pickle
import itertools
import twitconfig as cfg
pathToPheme = cfg.pheme_path
annotations = None


def loadAnnotations(path):
    """Returns annotation dataframe for all tweets in PHEME dataset

    Keyword arguments:
    path -- path to the location of the PHEME dataset
    """
    path += '\\PHEME\\pheme-rumour-scheme-dataset\\'
    path += 'annotations\\en-scheme-annotations.json'
    with open(path) as f:
        return pd.DataFrame(
            [json.loads(line) for line in f if '#' not in line]
        )


def crawlDirectory(path):
    """crawls PHEME directory and returns list of all conversation threads

    Keyword arguments:
    path -- path to directory
    """
    path += '\\PHEME\\pheme-rumour-scheme-dataset\\threads\\en'
    return list(itertools.chain.from_iterable(
        [t for t in [processCategory(path + '\\' + dirName)
                     for dirName in os.listdir(path)]]))


def processCategory(path):
    """Processes a PHEME tweet topic

    Keyword arguments:
    path -- path to the topics
    """
    return [processTweetFolder(path + '\\' + tweetFolder, tweetFolder)
            for tweetFolder in os.listdir(path)]


def processTweetFolder(path, tweetid):
    """Processes an entire thread and returns a tweet with all replies

    Keyword arguments:
    path -- path to threads
    tweetid -- tweetid of thread
    """
    thread = processTweetJSON(path + '\\source-tweets\\' +
                              tweetid + '.json', False)
    with open(path + '\\annotation.json') as f:
        thread.thread_annotation = json.load(f)
        thread.thread_annotation['tweetid'] = tweetid
    with open(path + '\\structure.json') as f:
        thread.thread_structure = json.load(f)
    root = Node(str(tweetid), tweet=thread)
    processTree(thread.thread_structure[tweetid], root, path + '\\reactions\\')
    thread.reply_chain = root
    thread.size = len(root.descendants)
    # print(RenderTree(root, style=AsciiStyle))
    thread.thread_id = tweetid
    return thread


def processTree(children, parent, path):
    """Returns tree of replies

    Keyword arguments:
    children -- dictionary of children remaining
    parent -- Node of parent
    """
    if not children:
        return
    for key, value in children.items():
        temp = Node(str(key), parent=parent,
                    tweet=processTweetJSON(path + key + '.json', True))
        processTree(value, temp, path)


def processTweetJSON(path, is_reply, labelled=True):
    """Processes and returns an individual tweet JSON

    Keyword arguments:
    path -- path to JSON
    is_reply -- boolean denoting whether tweet is a reply
    """
    from collections import namedtuple

    with open(path) as f:
        data = json.load(f)
        tweet = Tweet()
        tweet.phemeTweet(data)
        if labelled:
            tweet.annotation = annotations[
                annotations['tweetid'] == tweet.id
            ].to_dict('r')
        # keeps dataframe id out of the mix
        return tweet


def more_pheme():
    path = 'C:\\Users\\EECS\\Documents\\pheme-rnr-dataset'
    allTweets = []
    for topic in os.listdir(path):
        if not topic == 'README':
            allTweets += processTopic(os.path.join(path, topic), 'rumours')
            allTweets += processTopic(os.path.join(path, topic), 'non-rumours')
    return allTweets


def processTopic(path, type):
    topicTweets = []
    for tweet in os.listdir(os.path.join(path, type)):
        tempTweet = processTweetJSON(os.path.join(path, type, tweet,
                                                  'source-tweet',
                                                  tweet+'.json'),
                                     False, labelled=False
                                     )
        tempTweet.annotation = (type == 'rumours')
        tempTweet.thread_annotation = (type == 'rumours')
        root = Node(str(tempTweet.id), tweet=tempTweet)
        for reply in os.listdir(os.path.join(path, type, tweet, 'reactions')):
            tempReply = processTweetJSON(os.path.join(path, type, tweet,
                                                      'reactions', reply),
                                         False, labelled=False)
            tempNode = Node(str(tempReply.id), parent=root,
                            tweet=tempReply)
        tempTweet.reply_chain = root
        tempTweet.size = len(os.listdir(os.path.join(path, type, tweet,
                                                     'reactions'))) + 1
        topicTweets.append(tempTweet)
    return topicTweets


def parsePheme():
    """Parses PHEME dataset and returns a list of all conversation threads

    """
    global annotations
    annotations = loadAnnotations(pathToPheme)
    return crawlDirectory(pathToPheme) + more_pheme()

    # If input changes and you need to save the new correct input, uncomment
    # temp = crawlDirectory(pathToPheme)
    # with open('input_test.pkl', 'wb') as outfile:
    #    pickle.dump(temp, outfile, pickle.HIGHEST_PROTOCOL)
    # return temp
