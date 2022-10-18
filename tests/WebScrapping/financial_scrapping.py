import datetime
import pandas as pd
import snscrape.modules.twitter as scrapTwitter

"""
Teste para buscar informações no twitter em períodos de queda analisados.

"""


end_time = datetime.date.today()

start_time = '2022-10-11'

stock_enterprise = "RRRP3" # 3R

list_tweets_stock_enterprise = []

for indice, tweet in enumerate(scrapTwitter.TwitterSearchScraper(f'{stock_enterprise} + since:{start_time} until:{end_time}').get_items()):
    if indice > 500:
        break
    list_tweets_stock_enterprise.append([tweet.date, tweet.id, tweet.content, tweet.username])

tweets_dataframe = pd.DataFrame(list_tweets_stock_enterprise, columns=['tweet.date', 'tweet.id', 'tweet.content', 'tweet.username'])

print(tweets_dataframe)