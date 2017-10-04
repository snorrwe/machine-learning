#!/usr/bin/python
"""
Testing the Regression class
Run this from /knn/
like so: python -m src.regression.regression_test
"""
import random
import pandas as pd
import os
import sys
import unittest
import time
import json
from sklearn.metrics import mean_absolute_error
from src.regression.regression import Regression
import matplotlib as mpl
import numpy as np
mpl.use('Agg')
import matplotlib.pyplot as pyplot


HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, 'results', 'error_rates')
DATA = os.path.join(HERE, 'data')


class RegressionSanityTest(unittest.TestCase):
    def test_can_create(self):
        Regression()


class RegressionHousesTests(object):
    """
    Take in King County housing data, calculate and plot the kNN regression error rate.
    """

    def __init__(self):
        self.data = None
        self.values = None

    def load_csv_file(self, csv_file, columns, value_col, limit=None):
        """
        Loads CSV file with data data
        :param csv_file: CSV file name
        :param limit: number of rows of file to read
        """
        data = pd.read_csv(csv_file, nrows=limit)
        self.values = data[value_col]
        data = data.drop(value_col, 1)
        data = (data - data.mean()) / (data.max() - data.min())
        self.data = data[columns]

    def clear_nan(self, rows):
        return [x for x in rows if not np.isnan(x)]

    def plot_error_rates(self, count, outfile):
        """
        Plots MAE vs #folds
        """
        for i in range(count):
            folds_range = range(3, 11)
            errors_df = pd.DataFrame({'max': 0, 'min': 0}, index=folds_range)
            delta_times = {}
            for folds in folds_range:
                errors, times = self.tests(folds)
                errors_df['max'][folds] = max(errors)
                errors_df['min'][folds] = min(errors)
                delta_times[folds] = times
            errors_df.plot(title='Mean Absolute Error of KNN over different folds_range')
            pyplot.xlabel('#folds_range')
            pyplot.ylabel('MAE')
            fname = '%s_%s.png' % (outfile, i)
            fname = os.path.join(RESULTS, fname)
            pyplot.savefig(fname, dpi=None, facecolor='w', edgecolor='w',
                           orientation='portrait', papertype=None, format='png',
                           transparent=False, bbox_inches=None, pad_inches=0.1,
                           frameon=None)
            self.save_metadata(fname, errors_df, delta_times)

    def save_metadata(self, outfile, errors, delta_times):
        with open('%s.meta' % outfile, 'w+') as f:
            t = json.dumps(delta_times, indent=4)
            f.write("""{errors}

Delta Times = {times}
""".format(errors=errors, times=t))

    def tests(self, folds):
        """
        Calculates mean absolute errors for series of tests
        :param folds: how many times split the data
        :return: tuple of list of error values and list of time taken
        """
        holdout = 1.0 / folds
        errors = []
        times = []
        for _ in range(folds):
            t_start = time.clock()
            values_regress, values_actual = self.test_regression(holdout)
            errors.append(mean_absolute_error(values_actual, values_regress))
            times.append(time.clock() - t_start)
        return (errors, times)

    def test_regression(self, holdout):
        """
        Calculates regression for out-of-sample data
        :param holdout: part of the data for testing [0,1]
        :return: tuple(y_regression, values_actual)
        """
        test_rows = random.sample(self.data.index.tolist(),
                                  int(round(len(self.data) * holdout)))
        train_rows = set(range(len(self.data))) - set(test_rows)
        df_test = self.data.ix[test_rows]
        df_train = self.data.drop(test_rows)

        train_values = self.values.ix[train_rows]
        regression = Regression()
        regression.set_data(df_train, train_values)

        values_regr = []
        values_actual = []

        for idx, row in df_test.iterrows():
            values_regr.append(regression.regress(row))
            values_actual.append(self.values[idx])

        return values_regr, values_actual


def test_datas(directory, columns, value_col):
    data_path = os.path.join(DATA, directory)
    regression_test = RegressionHousesTests()
    for path in os.listdir(data_path):
        fpath = os.path.sep.join([data_path, path])
        regression_test.load_csv_file(fpath, columns, value_col, 100)
        regression_test.plot_error_rates(5, path)


def clean_results(directory):
    if not os.path.isdir(directory):
        os.makedirs(directory)
    else:
        for file in os.listdir(directory):
            os.remove(os.path.join(directory, file))


def main():
    sys.setrecursionlimit(10000)
    clean_results(RESULTS)
    test_datas('houses', ['lat', 'long', 'SqFtLot'], 'AppraisedValue')
    test_datas('cars', ["wheel-base", "length", "width", "height", "engine-size",
                        "stroke", "horsepower", "peak-rpm", "city-mpg", "highway-mpg"], 'price')


if __name__ == '__main__':
    main()
