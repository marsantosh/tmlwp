import numpy as np
import pandas as pd
from sklearn import tree
from sklearn import metrics
from sklearn import ensemble


class MushroomProblem:
    def __init__(self, data_file):
        self.dataFrame = pd.read_csv(data_file)
        for k in self.dataFrame.columns[1:]:
            self.dataFrame[k], __ = pd.factorize(self.dataFrame[k])
        
        sorted_cats = sorted(pd.Categorical(self.dataFrame['class']).categories)
        self.classes = np.array(sorted_cats)
        self.features = self.dataFrame.columns[self.dataFrame.columns != 'class']
    
    def __factorize(self, data):
        y, __ = pd.factorize(pd.Categorical(data['class']), sort = True)
        return y
    
    def validation_data(self, folds):
        df = self.dataFrame
        response = []
        
        assert len(df) > folds

        perms = np.array_split(np.random.permutation(len(df)), folds)

        for i in range(0, folds):
            train_idxs = list(range(0, folds))
            train_idxs.pop(i)
            train = []
            for idx in train_idxs:
                train.append(perms[idx])
    
            train = np.concatenate(train)
            test_idx = perms[i]

            training = df.iloc[train]
            test_data = df.iloc[test_idx]

            y = self.__factorize(training)
            classifier = self.train(training[self.features], y)
            predictions = classifier.predict(test_data[self.features])

            expected = self.__factorize(test_data)
            response.append([predictions, expected])
        
        return response


class MushroomRegression(MushroomProblem):
    def train(self, X, Y):
        reg = tree.DecisionTreeRegressor()
        reg = reg.fit(X, Y)
        return reg
    
    def validate(self, folds):
        responses = []

        for y_true, y_pred in self.validation_data(folds):
            responses.append(metrics.mean_squared_error(y_true, y_pred))
        return responses


class MushroomClassifier(MushroomProblem):
    def validate(self, folds):
        confusion_matrices = []
    
        for test, training in self.validation_data(folds):
            confusion_matrices.append(self.confusion_matrix(training, test))
        
        return confusion_matrices
    
    def confusion_matrix(self, train, test):
        return pd.crosstab(test, train, rownames = ['actual'], colnames = ['preds'])
    

class MushroomForest(MushroomClassifier):
    def train(self, X, Y):
        clf = ensemble.RandomForestClassifier(n_jobs = 2)
        clf = clf.git(X, Y)
        return clf


class MushroomTree(MushroomClassifier):
    def train(self, X, Y):
        clf = tree.DecisionTreeClassifier()
        clf = clf.fit(X, Y)
        return clf

