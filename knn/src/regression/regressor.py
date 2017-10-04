import sys
from scipy.spatial import KDTree
import numpy as np


class Regression(object):
    """
    Performs KNN regression
    """
    sys.setrecursionlimit(10000)

    def __init__(self):
        self.k = 5
        self.metric = np.mean
        self.data = None
        self.values = None
        self.kdtree = None

    def set_data(self, data, values, **kwargs):
        """
        Sets data and values
        :param data: pandas.DataFrame with object parameters
        :param values: pandas.Series with object values
        """
        self.data = data
        self.kdtree = KDTree(self.data)
        self.values = values
        if 'k' in kwargs:
            self.k = kwargs['k']

    def regress(self, query_point):
        """
        Calculates predicted value for object with particular parameters
        :param query_point: pandas.Series with object parameters
        :return: object value
        """
        _, indexes = self.kdtree.query(query_point, self.k)
        value = self.metric(self.values.iloc[indexes])
        if np.isnan(value):
            raise Exception('Unexpected result')
        return value
