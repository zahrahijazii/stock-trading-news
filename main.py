import requests
from datetime import date, timedelta
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
ACCOUNT_SID = "AC53ec109fd4521b121d3b8a25052aca93"
AUTH_TOKEN = "4a6b81a97ddbbcbf7a328e08194a129a"

api_key = "X7HDOZHKRUJK3HBO"

response = requests.get(f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={STOCK}&apikey={api_key}")
response.raise_for_status()
data = response.json()

news_response = requests.get(f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={STOCK}&apikey={api_key}")
news_response.raise_for_status()
news_data = news_response.json()


## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
yesterday_date = date.today() - timedelta(days=1)
yesterday_stock = float(data["Time Series (Daily)"][str(yesterday_date)]['4. close'])


previous_day = date.today() - timedelta(days=2)
previous_day_stock = float(data["Time Series (Daily)"][str(previous_day)]['4. close'])

percentage_difference = (abs(yesterday_stock - previous_day_stock) / yesterday_stock) * 100

def get_news(percentage):
    for i in range(0,3):
        news_title = news_data["feed"][i]["title"]
        news_brief = news_data["feed"][i]["summary"]
        return f"{STOCK}: {percentage}%\nHeadline:{news_title}\nBrief:{news_brief}\n\n"

if percentage_difference > 0 : 
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    message = client.messages \
                .create(
                    body=get_news(percentage_difference),
                    from_='+14706348198',
                    to='+14706348198'
                )
    print(message.sid)



