from tweet import *
from anytree import Node, RenderTree, AsciiStyle, LevelOrderIter

def follow_ratio(user):
    if user.friends_count == 0:
        print(user)
        return 0
    return (user.followers_count/user.friends_count)

def sentiment(tweet):
    import requests
    url = 'http://text-processing.com/api/sentiment'
    input = tweet.tweet_text
    payload = {'text': input}
    print(payload)
    r = requests.post(url, data=payload)
    print(r)
    output = r.json()
    pos = output['probability']['pos']
    neg = output['probability']['neg']
    neutral = output['probability']['neutral']
    return pos

def graph_weight(reply_chain, func):
    if reply_chain is None:
        return 0
    credAgg = 0
    weight = 1.0
    for node in LevelOrderIter(reply_chain):
        credAgg += weight*func(node.tweet.user)
        weight *= .5
    return credAgg

def convert_annotations(annotation, isString=True):
    if 'misinformation' in annotation.keys() and 'true'in annotation.keys():
        if int(annotation['misinformation']) == 0 and int(annotation['true']) == 0:
            if isString:
                label = "unverified"
            else:
                label = 2
        elif int(annotation['misinformation']) == 0 and int(annotation['true']) == 1:
            if isString:
                label = "true"
            else:
                label = 1
        elif int(annotation['misinformation']) == 1 and int(annotation['true']) == 0:
            if isString:
                label = "false"
            else:
                label = 0
        elif int(annotation['misinformation']) == 1 and int(annotation['true']) == 1:
            print("OMG! They both are 1!")
            print(annotation['misinformation'])
            print(annotation['true'])
            label = None

    elif 'misinformation' in annotation.keys() and 'true' not in annotation.keys():
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

    elif 'true' in annotation.keys() and 'misinformation' not in annotation.keys():
        print('Has true not misinformation')
        label = None
    else:
        print('No annotations')
        label = None

    return label
