import pandas as pd
import numpy as np
import phemeParser
import time
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import KFold
from features import *
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt

class Classifier:
    def __init__(self):
        self.threads = pd.Series(
            [t for t in phemeParser.parsePheme()]
        )
        self.model = MLPClassifier(solver='lbfgs')

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

        print(
            'average score for %s tests is %s' % (
                n_splits, totalScore/n_splits
            )
        )
        print('best score was %s\nworst score was %s' % (best, worst))
        if verbose:
            class_names = np.array(['false', 'true', 'unverified'])
            plot_confusion_matrix(y_true_best, y_pred_best, classes=class_names)
            plt.show()
            plot_confusion_matrix(y_true_worst, y_pred_worst, classes=class_names)
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

    def buildInput(self, data):
        """Outputs input vectors for unlabeled datasets

        Keyword arguments:
        data -- input list of threads
        """

        # This is where the features from features.py are integrated
        inputs = pd.DataFrame()
        inputs['follow_ratio'] = data.apply(follow_ratio)
        inputs['graph_follow_ratio'] = data.apply(
            lambda x: graph_weight(x, follow_ratio)
        )
        inputs['sentiment'] = data.apply(sentiment)
        return inputs

    def run(self, verb=False, testTweets=None):
        """Trains model and makes predictions for unlabeled set of tweets

        listOfThreads: input from PHEME to train datasets
        testTweets: list of Tweets to predict on
        """
        start_time = time.time()
        input, labels = self.buildInputAndLabels(self.threads)
        self.kfold(input, labels, n_splits=5, verbose=verb)
        if testTweets is not None:
            testX = self.buildInput(testTweets)
            self.model.predict(textX)

    def predict(self, tweet):
        probMap = {'false': 0, 'true': 1, 'unverified': 2}
        df = pd.Series([tweet])
        input = self.buildInput(df)
        prediction = self.model.predict(input)
        probMat = self.model.predict_proba(input)
        index = probMap[prediction[0]]
        prob = probMat[0, index]/np.sum(probMat[0])
        return prediction, prob

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
    # Only use the labels that appear in the data
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
