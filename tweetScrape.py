#!/usr/bin/env python
# coding: utf-8

# In[30]:


import tweepy
import pandas as pd
import numpy as np
import pyodbc
import secret


# In[31]:


#accessing the Twitter API
client = tweepy.Client(bearer_token = secret.BEARER)


# In[32]:


#specifying query for searching Twitter
query = 'Wordle 6 -is:retweet'

#searching tweets per the query
tweets = client.search_recent_tweets(query=query,max_results= 100, tweet_fields=['author_id', 'created_at','geo'])


# In[33]:


data = pd.DataFrame(data = [tweet.id for tweet in tweets.data], columns =['ID'])
data['Author'] = np.array([tweet.author_id for tweet in tweets.data])

data.head(10)


# In[34]:


score_arr = []
day_arr = []
isHard_arr = []

for tweet in tweets.data:
    score = tweet.text.find("/")-1

    if tweet.text[score].isnumeric():
        score_arr.append(tweet.text[score])
    else:
        score_arr.append(0)

    temp_day = tweet.text.partition("Wordle ")
    day = temp_day[2][0:4]

    if(day[0:3].isnumeric() and day[3] == " "):
        day_arr.append(day[0:3])
    else:
        day_arr.append('NaN')

    if(tweet.text[score+3] == '*'):
        isHard_arr.append(1)
    else:
        isHard_arr.append(0)


# In[35]:


data['WordleDay'] = day_arr
data['Score'] = score_arr
data['HardMode'] = isHard_arr


# In[36]:


clean_data = data[data['WordleDay'].str.contains("NaN") == False]

clean_data.head(10)


# In[37]:


#uploading dataframe to the databse
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=AUSTIN-PC\SQLEXPRESS;'
                      'Database=WordleAnalysis;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor()

for index, row in clean_data.iterrows():
    cursor.execute("INSERT INTO TwitterWordle (ID,Author,WordleDay,Score,HardMode) values(?,?,?,?,?)", row.ID, row.Author, row.WordleDay, row.Score, row.HardMode)
conn.commit()
cursor.close()

