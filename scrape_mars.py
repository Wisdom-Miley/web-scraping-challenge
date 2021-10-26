
import pandas as pd
from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from webdriver_manager.chrome import ChromeDriverManager
import time


# In[2]:


# Setup splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# # NASA Mars News

# In[3]:


url = 'https://redplanetscience.com/'
browser.visit(url)


# In[4]:


html = browser.html
soup = BeautifulSoup(html, 'html.parser')


# In[5]:


result = soup.find('div', class_="list_text")

news_title = result.text
news_p = result.find('div',class_="article_teaser_body").text

print(f"news_title: {news_title}")
print(f"news_p: {news_p}")


# # JPL Mars Space Images - Featured Image

# In[6]:


fig_url = 'https://spaceimages-mars.com/'
browser.visit(fig_url)


# In[7]:


fig_html = browser.html
mars_fig_soup = BeautifulSoup(fig_html, 'html.parser')


# In[8]:


# the large image is within the figue element with class = lede
fig = mars_fig_soup.body.find("img", class_="headerimage fade-in")

# create the full url
featured_fig_url = fig_url+fig['src']

print(featured_fig_url)


# # Mars Facts

# In[9]:


facts_url ='https://galaxyfacts-mars.com/'
tables = pd.read_html(facts_url)
tables


# In[10]:


table_df = tables[0]
table_df.columns = ["Description","Mars","Earth"]

table_df


# In[11]:


mars_df = table_df.to_html("table.html", border="1",justify="left")


# # Mars Hemispheres

# In[12]:


hemis_url = 'https://marshemispheres.com/'
browser.visit(hemis_url)


# In[13]:


hemis_html = browser.html
soup = BeautifulSoup(hemis_html, 'html.parser')


# In[20]:


items = soup.find_all("div", class_="item")

main_url = "https://marshemispheres.com/"
hemisphere_url = []

for item in items:
    hemisphere_url.append(f"{main_url}{item.find('a', class_='itemLink')['href']}")

print(*hemisphere_url, sep = "\n")


# In[21]:


hemis_fig_url = []
for url in hemisphere_url:
    browser.visit(url)
    himis_html = browser.html 
    soup = BeautifulSoup(himis_html, 'html.parser')
    fig_url = soup.find('img', class_="wide-image")['src']
    title = soup.find('h2', class_="title").text
   # Append the dictionary with the image url string and the hemisphere title to a list
    hemis_fig_url.append({"title":title,"fig_url":f"https://marshemispheres.com/{fig_url}"})
hemis_fig_url    

mars_info = {
        "mars_news": {
            "news_title": news_title,
            "news_p": news_p,
            },
        "mars_img": featured_fig_url,
        "mars_fact": mars_df,
        "mars_hemisphere": hemis_fig_url
    }
browser.quit()

print(mars_info)

# In[ ]:




