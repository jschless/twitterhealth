import pandas as pd
import numpy as np
import phemeParser
import time
from sklearn.neural_network import MLPClassifier
from sklearn import svm
from sklearn.linear_model import SGDClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn import tree
from sklearn.model_selection import KFold
from features import *
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
import time
import graphviz


class Classifier:
    def __init__(self, folds, model='MLP', timing=False, parse_data=False):
        self.timing = timing
        start = time.time()
        self.type = model
        if parse_data:
            self.threads = pd.Series(phemeParser.parsePheme())
            self.threads.to_pickle('raw_data.pkl')
        else:
            self.threads = pd.read_pickle('raw_data.pkl')
        if self.timing:
            print('Threads: ' + str(len(self.threads)))
            tweets = 0
            for thread in self.threads:
                tweets += thread.size
            print('Num tweets: ' + str(tweets))
        end = time.time()
        if self.timing:
            print('parsing time: ' + str(end - start))
        if model == 'MLP':
            self.model = MLPClassifier(
                solver='lbfgs',
                hidden_layer_sizes=(1000, 1000, 1000)
            )
            print('[info] Multi-Layer Perceptron Classifier')
        elif model == 'SVC':
            self.model = svm.SVC(gamma='scale')
            print('[info] Support Vector Machine Classifier')
        elif model == 'SGD':
            self.model = SGDClassifier(loss='hinge', penalty='l2', max_iter=5)
            print('[info] Stochastic Gradient Descent Classifier')
        elif model == 'NN':
            self.model = KNeighborsClassifier(n_neighbors=3)
            print('[info] Nearest Neighbors Classifier')
        elif model == 'GAUS':
            self.model = GaussianProcessClassifier()
            print('[info] Gaussian Process Classifier')
        elif model == 'TREE':
            self.model = tree.DecisionTreeClassifier()
            print('[info] Decision Tree Classifier')
        self.folds = folds
        print('[info] Validation: K-fold with %s folds' % self.folds)

    def kfold(self, X, y, verbose=False, n_splits=5):
        """Trains model using kfold cross validation

        Keyword arguments:
        mod -- the model to be trained
        X -- input matrix
        y -- output matrix
        n_splits -- optional number of splits to apply to dataset
        """
        totalScore = 0
        kf = KFold(n_splits=n_splits, shuffle=True)
        best, best_mod, y_pred_best, y_true_best = None, None, None, None
        worst, worst_mod, y_pred_worst, y_true_worst = None, None, None, None
        for train_index, test_index in kf.split(X):
            new_mod = self.model.fit(X.iloc[train_index], y.iloc[train_index])
            score = self.model.score(X.iloc[test_index], y.iloc[test_index])
            if best is None or score > best:
                best = score
                best_mod = new_mod
                y_pred_best = best_mod.predict(X.iloc[test_index])
                y_true_best = y.iloc[test_index].values
            if worst is None or score < worst:
                worst = score
                worst_mod = new_mod
                y_pred_worst = worst_mod.predict(X.iloc[test_index])
                y_true_worst = y.iloc[test_index].values

            totalScore += score
        print(classification_report(y_true_best, y_pred_best))
        print(confusion_matrix(y_true_best, y_pred_best))
        print(classification_report(y_true_worst, y_pred_worst))
        print(confusion_matrix(y_true_worst, y_pred_worst))
        if self.type == 'TREE':
            data = dict(zip(X.columns, best_mod.feature_importances_))
            plt.bar(range(len(data)), list(data.values()), align='center')
            plt.xticks(range(len(data)), list(data.keys()), rotation=90)
            plt.tight_layout()
            plt.xlabel('Features')
            plt.ylabel('Weight')
            plt.title('Features by Importance')
            plt.show()
        if verbose:
            class_names = np.array(['false', 'true', 'unverified'])
            plot_confusion_matrix(
                y_true_best, y_pred_best, classes=class_names
            )
            plt.show()
            plot_confusion_matrix(
                y_true_worst, y_pred_worst, classes=class_names
            )
            plt.show()

        self.model = best_mod

    def buildInputAndLabels(self, data, label='misinformation'):
        """Outputs input matrix and label matrix

        Keyword arguments:
        data -- list of threads
        """
        input = self.buildInput(data)
        labels = data.apply(convert_annotations)
        return input, labels

    def buildInput(self, data, live_data=False, load_pickle=True):
        """Outputs input vectors for unlabeled datasets

        Keyword arguments:
        data -- input list of threads
        """
        if load_pickle and not live_data:
            return pd.read_pickle('features_3.pkl')
        else:
            inputs = pd.DataFrame()

            for func in features:
                func_name = str(func).split(' ')[1]
                inputs[func_name] = data.apply(func)

            for func in features:
                func_name = str(func).split(' ')[1]
                inputs['graph_' + func_name] = data.apply(
                    lambda x: graph_weight(x, func)
                )
            inputs.to_pickle('features_4.pkl')
        return inputs

    def run(self, verb=False, testTweets=None):
        """Trains model and makes predictions for unlabeled set of tweets

        listOfThreads: input from PHEME to train datasets
        testTweets: list of Tweets to predict on
        """
        start = time.time()
        input, labels = self.buildInputAndLabels(self.threads)
        self.kfold(input, labels, n_splits=self.folds, verbose=verb)
        if testTweets is not None:
            testX = self.buildInput(testTweets)
            self.model.predict(textX)
        end = time.time()
        if self.timing:
            print('model training time: ' + str(end - start))

    def predict(self, tweet):
        start = time.time()
        probMap = {'false': 0, 'true': 1, 'unverified': 2}
        df = pd.Series([tweet])
        input = self.buildInput(df, live_data=True)
        prediction = self.model.predict(input)
        probMat = self.model.predict_proba(input)

        index = probMap[prediction[0]]
        prob = probMat[0, index]/np.sum(probMat[0])
        end = time.time()
        if self.timing:
            print('time to classify a tweet: ' + str(end - start))
        return index, prob


def plot_confusion_matrix(y_true, y_pred, classes,
                          normalize=False,
                          title=None,
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    https://scikit-learn.org/stable/auto_examples/model_selection/
    plot_confusion_matrix.html
    """
    if not title:
        if normalize:
            title = 'Normalized confusion matrix'
        else:
            title = 'Confusion matrix, without normalization'

    # Compute confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    false_positive = cm[0, 1]/(np.sum(cm[0]))
    print('false positive rate: ' + str(false_positive))
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    fig, ax = plt.subplots()
    im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
    ax.figure.colorbar(im, ax=ax)
    # We want to show all ticks...
    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           # ... and label them with the respective list entries
           xticklabels=classes, yticklabels=classes,
           title=title,
           ylabel='True label',
           xlabel='Predicted label')

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], fmt),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black")
    fig.tight_layout()
    return ax
