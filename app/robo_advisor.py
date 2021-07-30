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

    csv_header = ["timestamp", "open", "high", "low", "close", "volume"]

    #adapted from https://realpython.com/python-csv/
    with open(csv_file_path, "w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=csv_header)
    

        writer.writeheader()

        for r in rows:
            writer.writerow(r)


load_dotenv() # loads environment variables set in a ".env" file, including the value of the ALPHAVANTAGE_API_KEY variable

#adapted from screencast
api_key = os.environ.get("ALPHAVANTAGE_API_KEY")


if __name__ == "__main__":
    query = input("What is the ticker symbol of the security you would like information about? (Enter 'done' if you're finished querying): ")

 #adapted logic from https://opentechschool.github.io/python-beginners/en/logical_operators.html
    while (query != 'done'):
        
        if not (0 < len(query) < 5):
            print("Sorry! That ticker is invalid. Please try again!")
            exit()
        #adapted from https://stackoverflow.com/questions/19859282/check-if-a-string-contains-a-number
        elif any(q.isdigit() for q in query):
            print("Sorry! Tickers do not contains digits. Please try again!")
            exit()

        request_url = compile_url(query)

        parsed_response = get_response(request_url)

        transformed_response = transform_response(parsed_response)

        #adapted from https://github.com/ryanbeaudet/robo-advisor-project/blob/master/app/robo_advisor.py
        try:
            last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]
            print(last_refreshed)
        except KeyError:
            print("Sorry! Ticker could not be found. Please try again!")
            exit()

        #adapted from https://stackoverflow.com/questions/14524322/how-to-convert-a-date-string-to-different-format
        last_refreshed_new = datetime.datetime.strptime(last_refreshed, '%Y-%m-%d').strftime('%B %d, %Y')

        api_key = os.environ.get("ALPHAVANTAGE_API_KEY") #as highlight in the content of the exercise

        #adapted from Robo Advisor screencast
        tsd = parsed_response["Time Series (Daily)"]

        dates = list(tsd.keys())

        #adapted from https://stackoverflow.com/questions/17627531/sort-list-of-date-strings
        sorted(dates, key=lambda date: datetime.datetime.strptime(date, '%Y-%m-%d'))

        
        #adapted from screencast
        latest_day = dates[0]

        latest_price_usd = tsd[latest_day]["4. close"]

        high_prices = []
        low_prices = []

        #high prices adapted from screencast
        for date in dates:
            high_price = tsd[date]["2. high"]
            high_prices.append(float(high_price))
            low_price = tsd[date]["3. low"]
            low_prices.append(float(low_price))

        recent_high = max(high_prices)
        recent_low = min(low_prices)



        #adapted from screencast
        csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", str(query) + " prices.csv")

        write_to_csv(transformed_response, csv_file_path)

    
    # some simple investing benchmark
        benchmark_factor = 1.05
        benchmark = recent_low * benchmark_factor
        recommendation = ""
        justification = ""

        if (float(latest_price_usd) < benchmark):
            recommendation = "Buy!Buy!!Buy!!!"
            justification = "The security price seems to be closer to 52-week low and is likely to be undervalued."
        elif (float(latest_price_usd) > benchmark):
            recommendation = "Don't buy!!"
            justification = "The security price seems to be closer to 52-week high and is likely to be overvalued."

        

        

        
