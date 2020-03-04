import sys
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.spatial import KDTree
from sklearn.metrics import mean_absolute_error

sys.setrecursionlimit(10000)

class Regression:

    def __init__(self, csv_file = None, data = None, values = None):
        if (data is None and csv_file is not None):
            df = pd.read_csv(csv_file)
            self.values = df['AppraisedValue']
            df = df.drop('AppraisedValue', axis = 1)
            df = (df - df.mean()) / (df.max() - df.min())
            self.df = df
            self.df = self.df[['lat', 'long', 'SqFtLot']]
        elif (data is not None and values is not None):
            self.df = data
            self.values = values
        else:
            raise ValueError('Must have either csv_file or data set')

        self.n = len(self.df)
        self.kdtree = KDTree(self.df)
        self.metric = np.mean
        self.k = 5

    def regress(self, query_point):
        __, indexes = self.kdtree.query(query_point, self.k)
        value = self.metric(self.values.iloc[indexes])
        if np.isnan(value):
            raise Exception('Unexpected result')
        else:
            return value
    
    def error_rate(self, folds):
        print('[INFO]    Entered error_rate method...')
        holdout = 1 / float(folds)
        errors = []
        for fold in range(folds):
            y_hat, y_true = self.__validation_data(holdout)
            errors.append(mean_absolute_error(y_true, y_hat))
        
        return errors
    
    def __validation_data(self, holdout):
        # print(self.df.index.to_set(), int(round(len(self.df) * holdout)))
        print('[INFO]       Entered __validation_data method...')
        test_rows = random.sample(set(self.df.index.to_list()), int(round(len(self.df) * holdout)))
        train_rows = set(range(len(self.df))) - set(test_rows)
        df_test = self.df.loc[test_rows]
        df_train = self.df.drop(test_rows)
        test_values = self.values.loc[train_rows]
        train_values = self.values.loc[train_rows]
        kd = Regression(data = df_train, values = train_values)

        y_hat = []
        y_actual = []

        for idx, row in df_test.iterrows():
            y_hat.append(kd.regress(row))
            y_actual.append(self.values[idx])
            
        return (y_hat, y_actual)
    
    def plot_error_rates(self):
        folds = range(2, 11)
        errors = pd.DataFrame(
            {
                'max': 0,
                'min': 0
            },
            index = folds
        )
        for fold in folds:
            print(f'[INFO] Iterating over fold: {fold} / {max(folds)}')
            error_rates = self.error_rate(fold)
            errors['max'][fold] = max(error_rates)
            errors['min'][fold] = min(error_rates)
        print('[INFO] Plotting absolute error over folds...')
        errors.plot(title = 'Mean Absolute error of KNN over different folds')
        plt.show()


if __name__ == '__main__':
    regression_test = Regression(csv_file = 'input/king_country_data_geocoded.csv')
    regression_test.plot_error_rates()