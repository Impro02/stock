import requests
import json
import datetime

API_KEY = ""
BASE_URL = "https://www.alphavantage.co/query"
MONTHS_BACK = 3
TOP_N = 10


headers = {
    "User-Agent": "My User Agent 1.0",
    "Content-Type": "application/x-download",
    "Content-Lenght": "853397",
    "Content-Disposition": "attachment; filename=listing_status.csv",
}  # replace with your own user agent

# Get the date three months ago from today's date
three_months_ago = datetime.datetime.today() - datetime.timedelta(days=30 * MONTHS_BACK)

# Make a request to Alpha Vantage to retrieve all Paris-listed stocks
params = {"function": "LISTING_STATUS", "market": "EURONEXT.PAR", "apikey": API_KEY}
response = requests.get(
    BASE_URL,
    params=params,
    verify=False,
    timeout=(10, 30),
    headers=headers,
    # proxies=proxies,
)
response_json = json.loads(response.text)

# Create a list to store the stock symbols and their percentage increases
stock_data = []

# Loop through each stock symbol and retrieve its historical data
for stock in response_json["data"]:
    stock_symbol = stock["symbol"]

    # Make a request to Alpha Vantage to retrieve the historical stock data
    params = {
        "function": "TIME_SERIES_DAILY_ADJUSTED",
        "symbol": stock_symbol,
        "apikey": API_KEY,
    }
    response = requests.get(BASE_URL, params=params)
    response_json = json.loads(response.text)

    # Calculate the percentage increase over the last 3 months
    prices = response_json["Time Series (Daily)"]
    current_price = float(prices[list(prices.keys())[0]]["4. close"])
    three_months_ago_price = float(
        prices[three_months_ago.strftime("%Y-%m-%d")]["4. close"]
    )
    percent_increase = (
        (current_price - three_months_ago_price) / three_months_ago_price
    ) * 100

    # Add the stock symbol and percentage increase to the list
    stock_data.append({"symbol": stock_symbol, "increase": percent_increase})

# Sort the list by percentage increase in descending order and take the top N stocks
top_stocks = sorted(stock_data, key=lambda x: x["increase"], reverse=True)[:TOP_N]

# Print out the top N stocks and their percentage increases
print(
    f"Top {TOP_N} Paris stocks with the highest percentage increase over the last {MONTHS_BACK} months:"
)
for stock in top_stocks:
    print(f"{stock['symbol']}: {round(stock['increase'], 2)}%")
