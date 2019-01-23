'''
trains a neural network dataset according to engineered features
'''
import pandas as pd
import phemeParser
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import KFold
from pandas_ml import ConfusionMatrix
import matplotlib.pyplot as plt
pathToPheme = 'C:\\Users\\EECS\\Documents'
classificationMap = {'certain': 2, 'somewhat-certain':1, 'uncertain':0, 'underspecified': -1}

def crossValidation(X, y):
    print('todo')

def kfold(mod, X, y, n_splits=5):
    totalScore = 0
    kf = KFold(n_splits=n_splits)
    best = None
    bestMod = None
    worst = None
    confusionMat = None
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

def initializeDataset(data):
    inputs = pd.DataFrame.from_records([thread.to_dict() for thread in data if len(thread.annotation) > 0]).set_index('tweetid')
    labels = pd.DataFrame.from_dict([thread.annotation[0] for thread in data if len(thread.annotation) > 0], orient = 'columns').set_index('tweetid')

    combined = pd.concat([inputs, labels], axis=1, sort=False) #combines the inputs with their labels
    return combined

def buildInputAndLabels(data, label='certainty'):
    data = data.dropna(subset=[label])
    X = data[['favorite_count', 'retweet_count']]
    y = data[label].apply(lambda x: classificationMap[x])
    return X, y

def buildInput(data):
    return data[['favorite_count', 'retweet_count']]

def run(listOfThreads, testTweets):
    '''
    listOfThreads: input from PHEME to train datasets
    testTweets: list of Tweets to predict on
    '''
    data = initializeDataset(listOfThreads)
    X, y = buildInputAndLabels(data)
    clf = MLPClassifier(solver='lbfgs')
    model = kfold(clf, X, y, 5)
    if testTweets is not None:
        model.predict(listToDF(testTweets))

def listToDF(inList):
    return buildInput(pd.DataFrame.from_records([tweet.to_dict() for tweet in inList]))

def main(testTweets=None):
    threadList, tweetList = phemeParser.parsePheme(pathToPheme)
    run(tweetList, testTweets)
#main()
