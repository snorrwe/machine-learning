import csv
import os
import time
from datetime import datetime
import requests


HERE = os.path.dirname(os.path.abspath(__file__))


def get_delta(index, stocks, n):
    try:
        return (int(stocks[index]['price']) - int(stocks[index - n]['price']))
    except (KeyError, IndexError):
        return 0


def calculate_deltas(stocks):
    for i, stock in enumerate(stocks):
        stock['delta_1'] = get_delta(i, stocks, 1)
        stock['delta_2'] = get_delta(i, stocks, 2)
        stock['delta_3'] = get_delta(i, stocks, 3)
        stock['delta_4'] = get_delta(i, stocks, 4)
        stock['delta_5'] = get_delta(i, stocks, 5)
        stock['delta_6'] = get_delta(i, stocks, 6)
        stock['delta_7'] = get_delta(i, stocks, 7)
    return stocks


def pull_stocks(url, fname):
    result = requests.get(url)
    with open(os.path.join(HERE, 'data', fname), 'w') as f:
        prices = result.json()['data']['prices']
        prices = calculate_deltas(prices)
        writer = csv.DictWriter(f, prices[0].keys())
        writer.writeheader()
        for row in prices:
            t = row['time']
            t = datetime.strptime(t, '%Y-%m-%dT%H:%M:%SZ')
            t = int(time.mktime(t.timetuple()))
            row['time'] = t
            writer.writerow(row)


def main():
    pull_stocks('https://www.coinbase.com/api/v2/prices/BTC-HUF/historic?period=year', 'BTC-HUF-year.csv')
    pull_stocks('https://www.coinbase.com/api/v2/prices/BTC-HUF/historic?period=day', 'BTC-HUF-day.csv')


if __name__ == '__main__':
    main()
