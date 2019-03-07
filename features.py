from tweet import *
from anytree import Node, RenderTree, AsciiStyle, LevelOrderIter


def follow_ratio(tweet):
    user = tweet.user
    if user.friends_count == 0:
        print('[warning] user ' + str(user) + ' has zero friends')
        return 0
    return (user.followers_count/user.friends_count)


def tweet_sentiment(tweet):
    return sentiment(tweet.text)


def sentiment(text):
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    analyzer = SentimentIntensityAnalyzer()
    scores = analyzer.polarity_scores(text)
    sent = scores['pos']-scores['neg']
    return sent


def retweet_count(tweet):
    return tweet.retweet_count


def favorite_count(tweet):
    return tweet.favorite_count


def name_sentiment(tweet):
    return sentiment(tweet.user.name)


def description_sentiment(tweet):
    return sentiment(tweet.user.description)


def screen_name_sentiment(tweet):
    if tweet.user.screenName == None:
        return -1
    else:
        return sentiment(tweet.user.screen_name)


def verified(tweet):
    return 1 if tweet.user.verified else 0

features = [
        follow_ratio, tweet_sentiment, retweet_count, favorite_count, verified,
        name_sentiment, description_sentiment, screen_name_sentiment
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
