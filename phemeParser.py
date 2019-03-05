import json
import os
import pandas as pd
from pandas.io.json import json_normalize
from itertools import chain
from tweet import *
from anytree import Node, RenderTree, DoubleStyle, AsciiStyle
from pprint import pprint
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
    # TODO: replace with flatten
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


def processTweetJSON(path, is_reply):
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
        tweet.annotation = annotations[
            annotations['tweetid'] == tweet.id
        ].to_dict('r')
        # keeps dataframe id out of the mix
        return tweet


def parsePheme():
    """Parses PHEME dataset and returns a list of all conversation threads

    """
    global annotations
    annotations = loadAnnotations(pathToPheme)
    return crawlDirectory(pathToPheme)
