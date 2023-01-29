import yfinance as yf
import numpy as np
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)


tickers = yf.Tickers('aapl goog meta nflx amzn')
aapl_df = tickers.tickers['AAPL'].history(period="3mo").iloc[:,:6]
goog_df = tickers.tickers['GOOG'].history(period="3mo").iloc[:,:6]
meta_df = tickers.tickers['META'].history(period="3mo").iloc[:,:6]
nflx_df = tickers.tickers['NFLX'].history(period="3mo").iloc[:,:6]
amzn_df = tickers.tickers['AMZN'].history(period="3mo").iloc[:,:6]



#-------------/ACCESS DATA------------------------#
def get_user_data(user_choice : str):
    stock_data = tickers.tickers[user_choice].history(period="3mo").iloc[:,:6]
    return stock_data

user_choice = "AAPL" # change to dynamically update based on front-end input

stock_data = get_user_data(user_choice)
#-------------ACCESS DATA/------------------------#
import sys
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from newsapi.newsapi_client import NewsApiClient
from datetime import date, timedelta, datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf
from datetime import date, timedelta

sia = SentimentIntensityAnalyzer()
pd.set_option('display.max_colwidth',1000)


def get_sources(category = None):
  newsapi = NewsApiClient(api_key='a3e22d1084184642adc18fb1e5abed2a')
  sources = newsapi.get_sources()
  if category is not None:
    rez = [source['id'] for source in sources['sources'] if source['category'] == category and source['language'] == 'en']
  else:
    rez = [source['id'] for source in sources['sources'] if source['language'] == 'en']
  
  return rez

def get_articles_sentiments(keywrd, startd, sources_list = None, show_all_articles = False):
  newsapi = NewsApiClient(api_key='a3e22d1084184642adc18fb1e5abed2a')
  if type(startd)== str :
    my_date = datetime.strptime(startd,'%d-%b-%Y')
  else:
    my_date = startd
  #If the sources list is provided - use it
  if sources_list:
      articles = newsapi.get_everything(q = keywrd, from_param = my_date.isoformat(), to = (my_date + timedelta(days = 1)).isoformat(), language="en", sources = ",".join(sources_list), sort_by="relevancy", page_size = 100)
  else:
      articles = newsapi.get_everything(q = keywrd, from_param = my_date.isoformat(),to = (my_date + timedelta(days = 1)).isoformat(), language="en", sort_by="relevancy", page_size = 100)
  article_content = ''
  date_sentiments = {}
  date_sentiments_list = []
  seen = set()
  for article in articles['articles']:
    seen.add(str(article['title']))

    article_content = str(article['title']) + '. ' + str(article['description'])
    #Get the sentiment score
    sentiment = sia.polarity_scores(article_content)['compound']
  
    date_sentiments.setdefault(my_date, []).append(sentiment)
    date_sentiments_list.append((sentiment, article['url'], article['title'],article['description']))
    date_sentiments_l = sorted(date_sentiments_list, key = lambda tup: tup[0],reverse = True)
    sent_list = list(date_sentiments.values())[0]
    #Return a dataframe with all sentiment scores and articles  
  return pd.DataFrame(date_sentiments_list, columns=['Sentiment','URL','Title','Description'])
  
def presentAllSentiment():
    end_date = date.today()
    x = end_date.month
    y = end_date.year
    z = end_date.day+1
    if end_date.month == 1:
        x = 12
        y = end_date.year -1
    if (end_date.month % 2 != 0) & (z == 31):
        z = 30
    if (end_date.month%2 == 0) & (z == 30):
        x = end_date.month
        z = 1
    start_date = date(year=y, month=x, day=z)
    
    print('Start day = ', start_date)
    print('End day = ', end_date)
    
    current_day = start_date
    business_sources = get_sources('business')
    sentiment_all_score = []
    sentiment_business_score = []
    count = 0
    dates=[]
    while current_day <= end_date:
      dates.append(current_day)
      sentiments_all = get_articles_sentiments(keywrd= 'stock' , startd = current_day, sources_list = None, show_all_articles= True)
      sentiment_all_score.append(sentiments_all.mean())
      sentiments_business = get_articles_sentiments(keywrd= 'stock' , startd = current_day, sources_list = business_sources, show_all_articles= True)
      sentiment_business_score.append(sentiments_business.mean())
      current_day = current_day + timedelta(days=1)
    for onedate in dates:
        if str(onedate) == ("2023-01-16"):
            dates.remove(onedate)
            count+=1
        if (np.is_busday(np.datetime64(str(onedate)))) == False:
            dates.remove(onedate)
            count+=1
    sentiments = pd.DataFrame([dates,np.array(sentiment_all_score),np.array(sentiment_business_score)]).transpose()
    sentiments.columns =['Date','All_sources_sentiment','Business_sources_sentiment']
    sentiments['Date'] = pd.to_datetime(sentiments['Date'])
    sentiments['All_sources_sentiment'] = sentiments['All_sources_sentiment'].astype(float)
    sentiments['Business_sources_sentiment'] = sentiments['Business_sources_sentiment'].astype(float)
    sentiments = sentiments.drop(sentiments.tail(count).index)
    return(sentiments)  
#-------------/FEATURE GENERATION------------------------#

# Today Trend - Brios Olivares
def feature_today_trend(opening_price, closing_price):
    p_o = opening_price
    p_c = closing_price

    return "Uptrend" if p_c - p_o >= 0 else "Downtrend"
    
# Yesterday Trend - Brios Olivares
def feature_yesterday_trend(closing_prices):
    p_today_c = closing_prices[0] # today's close price
    p_yesterday_c = closing_prices[1] # yesterday's close price
    
    return "Uptrend" if p_today_c - p_yesterday_c >= 0 else "Downtrend"

# SMA (Simple Moving Average) - Mannendri Olivares
# Desc: Calculates the avg of a selected range of prices, usually closing prices
# by the # of periods in that range
# Formula: (P_1 + P_2  + P_3  + ... + P_n)/n
def feature_sma(prices, n = 14) -> float:
    sum = 0.0
    for price in prices:
        sum+=price
    average = sum/n
    return average

# RSI (Relative Strength Index) - Michael Tesfaye 🐐
# Desc: measure of momentum of a stock to identify whether it is overbought or oversold
# Ranges between 0-100, inclusive
# Formula: 100 - [100/(1 + rs))]
def average(prices) -> float:
    sum = 0.0
    for price in prices:
        sum += price
    average = sum/len(prices)
    return average


def feature_rsi(closing_prices, period = 14) -> float:
    # deltas = stock_data["Close"].diff()
    deltas = []
    for i, price in enumerate(closing_prices):
        if i == 0:
            deltas += [0]
        else:
            deltas += [price - closing_prices[i - 1]]
    
    gains = [delta if delta > 0 else 0 for delta in deltas]
    losses = [-delta if delta < 0 else 0 for delta in deltas]

    avg_gain = np.mean(gains[-period:])
    avg_loss = np.mean(losses[-period:])
    
    rs = avg_gain/avg_loss
    rsi = 100 - (100/(1 + rs))
    return rsi


# %K (Stochastic Oscillator indicator) - Joseph Oronto-Pratt
# Computes (in a similar manner to RSI) an indication of momentum of a stock for 
# seeing whether it is being overbought or oversold, but uses "support" and "resistance" levels. Default is n = 14 trading days
def feature_oscillator(closing_prices, low_prices, high_prices, n = 14) -> float:
    p_c = closing_prices[-1]
    lowest_low = min(low_prices[-n:])
    highest_high = max(high_prices[-n:])
    k = 100 * (p_c - lowest_low) / (highest_high - lowest_low)
    return k

# Invokes each feature function 
def generate_features(stock_data):
    closing_prices = list(stock_data.to_dict()['Open'].values()).reverse()
    opening_prices = list(stock_data.to_dict()['Close'].values()).reverse()
    low_prices = list(stock_data.to_dict()['Low'].values()).reverse()
    high_prices = list(stock_data.to_dict()['High'].values()).reverse()
    trends = []
    ytrends = []
    nrsi = []
    nsma = []
    nocsi = []
    for i in range (len(opening_prices)):
        trends.append(feature_today_trend(opening_prices[i], closing_prices[i]))
    for i in range(len(closing_prices)-2):
        ytrends.append(feature_yesterday_trend(closing_prices[i:i+2]))
    for i in range(len(closing_prices)-15):
        nrsi.append(feature_rsi((closing_prices[i:i+15])))
    for i in range(len(closing_prices)-15):
        nsma.append(feature_sma(closing_prices[i:i+15]))
    for i in range(len(closing_prices)-15):
        nocsi.append(feature_oscillator(closing_prices[i:i+15], low_prices[i:i+15], high_prices[i:i+15]))
    
    tdtrend = feature_today_trend(opening_prices, closing_prices)
    ystrend = feature_yesterday_trend(closing_prices)
    rsi = feature_rsi(closing_prices)
    sma = feature_sma(closing_prices)
    oscillator = feature_oscillator(closing_prices, low_prices, high_prices)
    
    features = {
        "tdtrend": tdtrend,
        "ystrend": ystrend,
        "rsi": rsi,
        "sma": sma,
        "oscillator": oscillator
    }
    return features



#-------------FEATURE GENERATION/------------------------#




#------RUN FLASK APP----------#
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
''''''
@app.route("/")
@app.route("/user-choice", methods=['GET', 'POST'])
def post_user_choice():
    if request.method == "POST":
        return render_template("index.html", ticker=request.form.get("tickers"))
    else:
        return render_template("index.html")


stock_data = get_user_data(post_user_choice())

# Apply feature generation
features = generate_features(stock_data)
print(features)
