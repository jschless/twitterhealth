import pandas as pd
import phemeParser
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import KFold
from pandas_ml import ConfusionMatrix
from features import *
import matplotlib.pyplot as plt
pathToPheme = 'C:\\Users\\EECS\\Documents'
certaintyMap = {'certain': 2, 'somewhat-certain':1, 'uncertain':0, 'underspecified': -1}

def crossValidation(X, y):
    print('todo')

def kfold(mod, X, y, n_splits=5):
    """Trains model using kfold cross validation

    Keyword arguments:
    mod -- the model to be trained
    X -- input matrix
    y -- output matrix
    n_splits -- optional number of splits to apply to dataset
    """

    totalScore = 0
    kf = KFold(n_splits=n_splits)
    best, bestMod, worst, confusionMat = None, None, None, None
    for train_index, test_index in kf.split(X):
        newMod = mod.fit(X.iloc[train_index], y.iloc[train_index])
        score = mod.score(X.iloc[test_index], y.iloc[test_index])
        if best == None or score > best:
            best = score
            bestMod = newMod
            predictionY = bestMod.predict(X.iloc[test_index])
            confusionMat = ConfusionMatrix(y.iloc[test_index].values, predictionY)
            #confusionMat.print_stats()
        if worst == None or score < best:
            worst = score
        totalScore += score

    print('average score for %s tests is %s' % (n_splits, totalScore/n_splits))
    print('best score was %s\n worst score was %s' % (best, worst))
    confusionMat.plot()
    plt.show()
    return bestMod


def buildInputAndLabels(data, label='misinformation'):
    """Outputs input matrix and label matrix

    Keyword arguments:
    data -- list of threads
    """
    X = buildInput(data)
    labels = pd.DataFrame.from_dict([thread.thread_annotation for thread in data if len(thread.thread_annotation) > 0], orient = 'columns').set_index('tweetid')
    #combined = pd.concat([inputs, labels], axis=1, sort=False) #combines the inputs with their labels
    y = labels[label].apply(lambda x: int(x)) #.apply(lambda x: classificationMap[x])
    return X, y

def buildInput(data):
    """Outputs input vectors for unlabeled datasets

    Keyword arguments:
    data -- input list of threads
    """

    """This is where the features from features.py are integrated"""
    inputs = pd.DataFrame()
    inputs['follow_ratio'] = [follow_ratio(thread.user) for thread in data]
    #inputs['sentiment'] = [sentiment(thread) for thread in data]
    return inputs

def run(listOfThreads, testTweets):
    """Trains model and makes predictions for unlabeled set of tweets


    listOfThreads: input from PHEME to train datasets
    testTweets: list of Tweets to predict on
    """
    X, y = buildInputAndLabels(listOfThreads)
    clf = MLPClassifier(solver='lbfgs')
    model = kfold(clf, X, y, 5)
    if testTweets is not None:
        model.predict(listToDF(testTweets))

def listToDF(inList):
    """Turns a list of tweets to a pandas dataframe"""
    return buildInput(pd.DataFrame.from_records([tweet.to_dict() for tweet in inList]))

def main(testTweets=None):
    threadList = phemeParser.parsePheme(pathToPheme)
    run(threadList, testTweets)
main()
