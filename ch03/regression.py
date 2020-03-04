import sys
import random
import numpy as np
import pandas as pd
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
        self.metric = np.nean
        self.k = 5
