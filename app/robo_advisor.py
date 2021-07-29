from dotenv import load_dotenv
import json
import csv
import os
import requests
import datetime

#adapted from Crunch the data exercise
def to_usd(price):
    return "${0:,.2f}".format(price)


#adapted from "https://github.com/ryanbeaudet/robo-advisor-project/blob/master/app/robo_advisor.py"
def compile_url(ticker):
    request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + str(ticker) + "&apikey=" + str(api_key)
    return request_url


#adapted from https://github.com/prof-rossetti/robo-advisor-demo-2019/blob/master/app/robo_advisor.py
def get_response(request_url):
    #adapted from the screencast
    response = requests.get(request_url)
    print(response)
    parsed_response = json.loads(response.text)

    return parsed_response


#adapted from https://github.com/prof-rossetti/robo-advisor-demo-2019/blob/master/app/robo_advisor.py
def transform_response(parsed_response):
    dates = parsed_response["Time Series (Daily)"]

    rows = []

    for date, daily_prices in dates.items():
        row = {
            "timestamp": date,
            "open": daily_prices["1. open"],
            "high": daily_prices["2. high"],
            "low": daily_prices["3. low"],
            "close": daily_prices["4. close"],
            "volume": daily_prices["5. volume"]
        }
        rows.append(row)
    
    return rows

#adapted from https://github.com/prof-rossetti/robo-advisor-demo-2019/blob/master/app/robo_advisor.py
def write_to_csv(rows, csv_filepath):

    csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]

    #adapted from https://realpython.com/python-csv/
    with open(csv_file_path, "w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=csv_headers)

        writer.writeheader()

        for r in rows:
            writer.writerow(r)



load_dotenv() # loads environment variables set in a ".env" file, including the value of the ALPHAVANTAGE_API_KEY variable

#adapted from screencast
api_key = os.environ.get("ALPHAVANTAGE_API_KEY")


if __name__ == "__main__":
    query = input("What is the ticker symbol of the security you would like information about? (Enter 'done' if you're finished querying): ")

