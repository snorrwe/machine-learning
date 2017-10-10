#!/usr/bin/python
import pandas as pd
import os
from knn.src.regression.regressor import Regressor
from .get_stocks import main as get_stocks
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as pyplot


HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, 'results')
DATAS = [
    os.path.join(HERE, 'data', 'BTC-HUF-day.csv'),
    os.path.join(HERE, 'data', 'BTC-HUF-year.csv')
]


def load_data(csv_file, columns, value_col, limit=10000):
    data = pd.read_csv(csv_file, nrows=limit)
    values = data[value_col]
    data = data.drop(value_col, 1)
    data = (data - data.mean()) / (data.max() - data.min())
    return (data[columns], values)


def test(data, values, run_indexes, regressor, index, row, errors):
    try:
        run_indexes.append(index)
        result = regressor.regress(row)
        errors.append(result - values[index])
    except IndexError:
        pass
    finally:
        regressor.set_data(data.ix[run_indexes], values.ix[run_indexes])


def run_tests(data, values, training_count=1):
    errors = []
    regressor = Regressor()
    run_indexes = range(training_count)
    regressor.set_data(data.ix[run_indexes], values.ix[run_indexes])
    iterator = data.iterrows()
    for _ in run_indexes:
        iterator.next()
    for index, row in iterator:
        test(data, values, run_indexes, regressor, index, row, errors)
    return errors


def plot_errors(errors, outfile):
    pyplot.xlabel('Time')
    pyplot.ylabel('Error')
    abs_errors = map(lambda x: abs(x), errors)
    errors_df = pd.DataFrame({'abs_error': abs_errors}, index=range(len(errors)))
    errors_df.plot(title='')
    fname = '%s.png' % outfile
    fname = os.path.join(RESULTS, fname)
    pyplot.savefig(fname, dpi=None, facecolor='w', edgecolor='w',
                   orientation='portrait', papertype=None, format='png',
                   transparent=False, bbox_inches=None, pad_inches=0.1,
                   frameon=None)


def main():
    for DATA in DATAS:
        (data, values) = load_data(DATA,
                                   [
                                       'time',
                                       'delta_1',
                                       'delta_2',
                                       'delta_3',
                                       'delta_4',
                                       'delta_5',
                                       'delta_6',
                                       'delta_7'
                                   ],
                                   'price')
        errors = run_tests(data, values)
        output = DATA.split('/')[-1]
        output = output.replace(".csv", "")
        error_rates = {'errors': errors, 'error_percentile': []}
        for index, error in enumerate(errors):
            error_rates['error_percentile'].append(error / values[index] * 100.0)
        plot_errors(error_rates['errors'], output + "_scalar")
        plot_errors(error_rates['error_percentile'], output + "_percentile")


if __name__ == '__main__':
    get_stocks()
    main()
