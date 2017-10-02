#!/usr/bin/python
import random
import pandas as pd
import os
import sys
import unittest
from sklearn.metrics import mean_absolute_error
from .regression import Regression
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as pyplot

HERE = os.path.dirname(os.path.abspath(__file__))


class RegressionSanityTest(unittest.TestCase):
    def test_can_create(self):
        Regression()


class RegressionTest(object):
    """
    Take in King County housing data, calculate and plot the kNN regression error rate.
    """

    def __init__(self):
        self.houses = None
        self.values = None

    def load_csv_file(self, csv_file, limit=None):
        """
        Loads CSV file with houses data
        :param csv_file: CSV file name
        :param limit: number of rows of file to read
        """
        houses = pd.read_csv(csv_file, nrows=limit)
        self.values = houses['AppraisedValue']
        houses = houses.drop('AppraisedValue', 1)
        houses = (houses - houses.mean()) / (houses.max() - houses.min())
        self.houses = houses[['lat', 'long', 'SqFtLot']]

    def plot_error_rates(self, count, outfile):
        """
        Plots MAE vs #folds
        """
        for i in range(count):
            folds_range = range(3, 11)
            errors_df = pd.DataFrame({'max': 0, 'min': 0}, index=folds_range)
            for folds in folds_range:
                errors = self.tests(folds)
                errors_df['max'][folds] = max(errors)
                errors_df['min'][folds] = min(errors)
            errors_df.plot(title='Mean Absolute Error of KNN over different folds_range')
            pyplot.xlabel('#folds_range')
            pyplot.ylabel('MAE')
            pyplot.savefig('results/%s_%s.png' % (outfile, i), dpi=None, facecolor='w', edgecolor='w',
                           orientation='portrait', papertype=None, format='png',
                           transparent=False, bbox_inches=None, pad_inches=0.1,
                           frameon=None)

    def tests(self, folds):
        """
        Calculates mean absolute errors for series of tests
        :param folds: how many times split the data
        :return: list of error values
        """
        holdout = 1 / float(folds)
        errors = []
        for _ in range(folds):
            values_regress, values_actual = self.test_regression(holdout)
            errors.append(mean_absolute_error(values_actual, values_regress))

        return errors

    def test_regression(self, holdout):
        """
        Calculates regression for out-of-sample data
        :param holdout: part of the data for testing [0,1]
        :return: tuple(y_regression, values_actual)
        """
        test_rows = random.sample(self.houses.index.tolist(),
                                  int(round(len(self.houses) * holdout)))
        train_rows = set(range(len(self.houses))) - set(test_rows)
        df_test = self.houses.ix[test_rows]
        df_train = self.houses.drop(test_rows)

        train_values = self.values.ix[train_rows]
        regression = Regression()
        regression.set_data(df_train, train_values)

        values_regr = []
        values_actual = []

        for idx, row in df_test.iterrows():
            values_regr.append(regression.regress(row))
            values_actual.append(self.values[idx])

        return values_regr, values_actual


def main():
    sys.setrecursionlimit(10000)
    regression_test = RegressionTest()
    data_path = os.path.sep.join([HERE, '..', '..', 'data'])
    for path in os.listdir(data_path):
        fpath = os.path.sep.join([data_path, path])
        regression_test.load_csv_file(fpath, 1000)
        regression_test.plot_error_rates(5, path)


if __name__ == '__main__':
    main()
