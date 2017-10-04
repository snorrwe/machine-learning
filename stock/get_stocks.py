import csv
import time
from datetime import datetime
import requests


def main():
    result = requests.get('https://www.coinbase.com/api/v2/prices/BTC-HUF/historic?period=year')
    with open('BTC-HUF.csv', 'w') as f:
        prices = result.json()['data']['prices']
        writer = csv.DictWriter(f, prices[0].keys())
        writer.writeheader()
        for row in prices:
            t = row['time']
            t = datetime.strptime(t, '%Y-%m-%dT%H:%M:%SZ')
            t = int(time.mktime(t.timetuple()))
            row['time'] = t
            writer.writerow(row)


if __name__ == '__main__':
    main()
