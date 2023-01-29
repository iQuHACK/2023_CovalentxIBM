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
  newsapi = NewsApiClient(api_key='dbf4e99638574bf1832fbeb2b859f1c1')
  sources = newsapi.get_sources()
  if category is not None:
    rez = [source['id'] for source in sources['sources'] if source['category'] == category and source['language'] == 'en']
  else:
    rez = [source['id'] for source in sources['sources'] if source['language'] == 'en']
  
  return rez


def get_articles_sentiments(keywrd, startd, sources_list = None, show_all_articles = False):
  newsapi = NewsApiClient(api_key='dbf4e99638574bf1832fbeb2b859f1c1')
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