from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.base import BaseEstimator, ClassifierMixin
import numpy as np


class CustomClassifier(BaseEstimator, ClassifierMixin):
    """An example of classifier"""

    def __init__(self):
        self.mlp = Pipeline([
            ('tfidf', TfidfVectorizer(max_df=0.2,
                                      min_df=5,
                                      ngram_range=(1, 2),
                                      smooth_idf=True,
                                      strip_accents='ascii',
                                      sublinear_tf=False,
                                      use_idf=False)),
            ('clf', MLPClassifier(activation='logistic', alpha=0, solver='lbfgs')),
        ])
        self.rf = Pipeline([
            ('tfidf', TfidfVectorizer(max_df=0.2,
                                      min_df=2,
                                      ngram_range=(1, 1),
                                      smooth_idf=False,
                                      strip_accents='ascii',
                                      sublinear_tf=True,
                                      use_idf=True)),
            ('clf', RandomForestClassifier(max_depth=None,
                                           min_samples_leaf=1, min_samples_split=2, n_estimators=100)),
        ])
        self.svc = Pipeline([
            ('tfidf', TfidfVectorizer(max_df=0.6,
                                      min_df=1,
                                      ngram_range=(1, 1),
                                      smooth_idf=True,
                                      strip_accents='ascii',
                                      sublinear_tf=False,
                                      use_idf=True)),
            ('clf', SVC(C=4, kernel='linear', probability=True, shrinking=True, tol=1)),
        ])

        self.classifiers = [self.rf, self.mlp, self.svc]

    def fit(self, X, y=None):
        for classifier in self.classifiers:
            classifier.fit(X, y)
        return self

    def predict(self, X, y=None):
        try:
            result = []
            for item in X:
                partial_result = 0
                for classifier in self.classifiers:
                    if(classifier.predict([item]) == 1):
                      partial_result = 1
                result.append(partial_result)

        except AttributeError:
            raise RuntimeError(
                "You must train classifer before predicting data!")

        return result

    def score(self, X, y=None):
        return(sum(self.predict(X)))
