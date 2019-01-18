'''
trains a neural network dataset according to engineered features
'''
import pandas as pd
import phemeParser
from sklearn.neural_network import MLPClassifier

pathToPheme = 'C:\\Users\\EECS\\Documents'
classificationMap = {'certain': 2, 'somewhat-certain':1, 'uncertain':0, 'underspecified': -1}

def initializeInput(listOfThreads):
    X = pd.DataFrame.from_records([thread.to_dict() for thread in listOfThreads])
    return X[['favorite_count', 'ret_count']]

def initializeOutput(listOfThreads):
    y = pd.DataFrame.from_dict([thread.annotation[0] for thread in listOfThreads], orient = 'columns')
    y['certainty'] = y['certainty'].apply(lambda x: classificationMap[x])
    return y['certainty']

def crossValidation(X, y):
    print('todo')
    # for selecting hyperparameters TODO

def run(listOfThreads):
    X = initializeInput(listOfThreads)
    y = initializeOutput(listOfThreads)
    clf = MLPClassifier(solver='lbfgs')
    clf.fit(X, y)
    print('score is ' + str(clf.score(X,y)))

def main():
    threadList, tweetList = phemeParser.parsePheme(pathToPheme)
    run(threadList)

main()
