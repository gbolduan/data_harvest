#!/usr/bin/env python
# coding: utf-8

# ### Version 0.3, started July 18 in 2021

# In[5]:


import requests
from bs4 import BeautifulSoup
import pandas as pd


# In[6]:


response = requests.get("https://cispa.de/en/news-and-events/news-archive")
page = BeautifulSoup(response.text, 'html.parser')


# In[9]:


# getting to how much news-sites are there 
number_retrieved = page.select(".pagination")[1].get('data-pagesize')
number = int(number_retrieved)
# testing 
# number 


# In[11]:


# generating the list to automate URL construction
number_of_pages = list(range(1,number+1))

# testing: does it contain all numbers I need? From 1 to number+1 because of range()
# number_of_pages 


# In[12]:


# create a list urls that specifiy the webpages, the archive consists of
# I use a list comprehension🙈 

newspages_list = [f'https://cispa.de/en/news-and-events/news-archive?newsPage={page_var}#_news' for page_var in number_of_pages]

# testing: does it contain all URls? 
# newspages_list


# In[13]:


# scraping every website of the archive with the following code

# initializing the list for the results
scraped_news = []

for newspage in newspages_list:
    # initializing list to test 
    test_list = []
    # print(newspage)
    # requesting one of the needed URLs
    response = requests.get(newspage)
    # each url leads to a website of the news archive I want to scrape
    page = BeautifulSoup(response.text, 'html.parser')
    # on this website I am interested in the class .news as it contains information
    # about title, date and URL of each news
    articles  = page.select(".news")
    
    # debugging: test line 
    #print(f'++++++ list has {len(articles)} elements ++++++')
    
    # for every news on a webpage I scrape date, title, URL to full test of news  
    for article in articles: 
        # initializing the dictionary using to store scraped information
        a_news = {}
        date = article.select(".h2")[0].text.strip()
        title = article.get('title')
        url = article.get('href')
        # filling the structure of the dictionary a_news with values  
        a_news['date'] = date
        a_news['title'] = title
        a_news['url'] = url
        # playing around with the list
        test_list = [date, title, url]
        
        # putting a_news dictionary entry in the list of scraped_news
        scraped_news.append(a_news)

#         
# testing the filling         
#for item in scraped_news: 
 #   print('START')
  #  print(item)
   # print('END')

# testing the coverage: did I get all news? 
# print(len(scraped_news))


# In[14]:


# putting the scraped stuff into a dataframe
df = pd.DataFrame(scraped_news)
# hoch does the dataframe df look? 
#df


# In[15]:


# writing the dataframe df to a comma-separated values (csv) file
df.to_csv("scraped_news.csv")

