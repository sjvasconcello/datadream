# Getting Data
import csv
from collections import Counter


def get_domain(email_address: str) -> str:
    # Split on '@' and return the last piece
    return email_address.lower().split("@")[-1]


def process(date, symbol, price):
    print(date, symbol, price)


assert get_domain(
    "santiago.vasconcello@deutschebank.com") == "deutschebank.com"

print("Tab delimited stock prices:\n")
with open("data/tab_delimited_stock_prices.txt",
          "r", encoding='utf8', newline="") as f:
    tab_reader = csv.reader(f, delimiter='\t')
    for row in tab_reader:
        date = row[0]
        symbol = row[1]
        closing_price = float(row[2])
        process(date, symbol, closing_price)
print("\n")

print("Colon delimited stock prices:\n")
with open("data/colon_delimited_stock_prices.txt",
          "r",
          encoding='utf8',
          newline='') as f:
    colon_reader = csv.DictReader(f, delimiter=':')
    for row in colon_reader:
        date = row["date"]
        symbol = row["symbol"]
        closing_price = row["closing_price"]
        process(date, symbol, closing_price)
print("\n")

todays_prices = {'AAPL': 90.91, 'MSFT': 41.68, 'FB': 64.5}

with open('comma_delimited_stock_price.txt',
          'w',
          encoding='utf8',
          newline='') as f:
    csv_write = csv.writer(f, delimiter=',')
    for stock, price in todays_prices.items():
        csv_write.writerow([stock, price])
