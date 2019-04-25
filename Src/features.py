from tweet import *
from anytree import Node, RenderTree, AsciiStyle, LevelOrderIter
import pickle


def follow_rat(tweet):
    user = tweet.user
    if user.friends_count == 0:
        # print('[warning] user ' + str(user) + ' has zero friends')
        return user.followers_count
    return (user.followers_count/user.friends_count)


def tweet_sent(tweet):
    return sentiment(tweet.text)


def sentiment(text):
    if text is None:
        return 0
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    analyzer = SentimentIntensityAnalyzer()
    scores = analyzer.polarity_scores(text)
    sent = scores['pos']-scores['neg']
    return sent


def retweets(tweet):
    return tweet.retweet_count


def favorites(tweet):
    return tweet.favorite_count


def name_sent(tweet):
    return sentiment(tweet.user.name)


def desc_sent(tweet):
    return sentiment(tweet.user.description)


def s_name_sent(tweet):
    return sentiment(tweet.user.screen_name)


def verified(tweet):
    return 1 if tweet.user.verified else 0


features = [
        follow_rat, tweet_sent, retweets, favorites, verified,
        name_sent, desc_sent, s_name_sent
    ]


def graph_weight(tweet, func):
    reply_chain = tweet.reply_chain
    if reply_chain is None:
        return 0
    credAgg = 0
    weight = 1.0
    for node in LevelOrderIter(reply_chain):
        credAgg += weight*func(node.tweet)
        weight *= .5
    return credAgg


def convert_annotations(tweet, isString=True):
    annotation = tweet.thread_annotation

    if isinstance(annotation, bool):
        if annotation:
            if isString:
                label = "true"
            else:
                label = 1
        else:
            if isString:
                label = "false"
            else:
                label = 0
        return label
    if 'misinformation' in annotation.keys() and 'true'in annotation.keys():
        if (
            int(annotation['misinformation']) == 0 and
            int(annotation['true']) == 0
        ):
            if isString:
                label = "unverified"
            else:
                label = 2
        elif (
            int(annotation['misinformation']) == 0 and
            int(annotation['true']) == 1
        ):
            if isString:
                label = "true"
            else:
                label = 1
        elif (
            int(annotation['misinformation']) == 1 and
            int(annotation['true']) == 0
        ):
            if isString:
                label = "false"
            else:
                label = 0
        elif (
            int(annotation['misinformation']) == 1 and
            int(annotation['true']) == 1
        ):
            print("OMG! They both are 1!")
            print(annotation['misinformation'])
            print(annotation['true'])
            label = None

    elif (
        'misinformation' in annotation.keys() and
        'true' not in annotation.keys()
    ):
        # all instances have misinfo label but don't have true label
        if int(annotation['misinformation']) == 0:
            if isString:
                label = "unverified"
            else:
                label = 2
        elif int(annotation['misinformation']) == 1:
            if isString:
                label = "false"
            else:
                label = 0

    elif (
        'true' in annotation.keys() and
        'misinformation' not in annotation.keys()
    ):
        print('Has true not misinformation')
        label = None
    else:
        print('No annotations')
        label = None

    return label
