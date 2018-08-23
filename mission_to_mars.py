
# coding: utf-8

# ### Libraries used

# In[1]:


# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time
###import requests
###import pymongo
###import os
###import datetime as dt
###from selenium import webdriver


# In[2]:


executable_path = {"executable_path": "chromedriver.exe"}
browser = Browser("chrome", **executable_path, headless=True)
time.sleep(2)


# # Web Scraping:

# ## Nasa Mars News

# In[3]:


# URL of NASA Mars site, News page to be scraped
mars_url = 'https://mars.nasa.gov/news/'
browser.visit(mars_url)


# In[4]:


# Get HTML page with the browser; create BeautifulSoup object; parse with 'html.parser'
mars_html = browser.html
mars_nasa_data = BeautifulSoup(mars_html, 'html.parser')
#mars_nasa_data

# Get needed fields from html page, wait a second
# browser.is_element_present_by_css("ul.item_list li.slide",wait_time=1)
time.sleep(2)


# In[5]:


# Extract the first news title and description

# Get news_title and news_teaser_body

try:
    ###article_element = mars_nasa_data.select_one("ul.item_list li.slide")
    # print(f"The article_element is: {article_element}") 
    
    ###news_title = article_element.find("div", class_="content_title").get_text()
    news_title = mars_nasa_data.find('ul', class_="item_list").find('li',class_="slide").find('div',class_="content_title").text
    print(f"The news_title is: {news_title}") 
    
    ###news_teaser_body = article_element.find("div", class_="article_teaser_body").get_text()
    news_teaser_body = mars_nasa_data.find('ul',class_="item_list").find('li',class_="slide").find('div',class_="article_teaser_body").text
    print(f"The news teaser body is: {news_teaser_body}")
    
except AttributeError as e:
    print(e)


# ## JPG Mars Space Images - Featured Space Image

# In[6]:


# URL of NASA Mars site, JPL Featured Space Images page to be scraped
mar_space_images_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(mar_space_images_url)


# In[7]:


# Find and Click "FULL IMAGE" button
full_image_data = browser.find_by_id('full_image')
full_image_data.click()


# In[8]:


# Find and Click 'more info' button, wait a second
### browser.is_element_present_by_text('more info',wait_time=1)
time.sleep(5)
more_info_data = browser.find_link_by_partial_text('more info')
more_info_data.click()


# In[9]:


# Get HTML page with the browser; create BeautifulSoup object; parse with 'html.parser'
time.sleep(2)
mars_images_html = browser.html
mars_images_data = BeautifulSoup(mars_images_html, 'html.parser')
#mars_images_data


# In[10]:


# Get featured_image_url
try:    
    featured_image_url = mars_images_data.find('figure', class_='lede').a['href']
    print(f"The featured_image_url is: {featured_image_url}") 
    
except AttributeError as e:
    print(e)


# In[11]:


# Compose complete url string for this full size image png
full_image_url = "https://www.jpl.nasa.gov" + featured_image_url
print(f"The full_image_url is: {full_image_url}") 


# ## Mars Weather

# In[12]:


# URL of Mars Weather twitter page to be scraped
mars_twitter_weather_url = 'https://twitter.com/marswxreport?lang=en)'
browser.visit(mars_twitter_weather_url)


# In[13]:


# Get HTML page with the browser; create BeautifulSoup object; parse with 'html.parser'
mars_weather_html = browser.html
mars_weather_data = BeautifulSoup(mars_weather_html, 'html.parser')
#mars_weather_data


# In[14]:


# Scrape the latest Mars Weather tweet text
mars_weather  = mars_weather_data.find('div', attrs={"class": "tweet", "data-name": "Mars Weather"}).find('p',class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
print(f"The mars_weather is: {mars_weather}") 


# ## Mars Facts

# In[15]:


# Read Mars Facts webpage; use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
mars_facts_url = 'https://space-facts.com/mars/'
mars_facts_table_df = pd.read_html(mars_facts_url)[0]
mars_facts_table_df.columns = ['Description','Value']
mars_facts_table_df


# In[16]:


# Use Pandas to convert the data to a HTML table string and save to a file
mars_facts_table_df.to_html('MarsFactsTable.html', index=False )
#mars_facts_table_df.to_html()


# ## Mars Hemispheres

# In[17]:


# URL of USGS Astrogeology site to be scraped
# to obtain high resolution images for each of Mar's hemispheres
usgs_astrogeology_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(usgs_astrogeology_url)

# Initialize the list for the dictionary of hemisphere images 
hemisphere_image_urls = []

# Get HTML page with the browser; create BeautifulSoup object; parse with 'html.parser'
usgs_astrogeology_html = browser.html
all_hemisphere_data = BeautifulSoup(usgs_astrogeology_html, 'html.parser')
#all_hemisphere_data


# In[18]:


# Get the iterable list of all hemispere information
hemisphere_results = all_hemisphere_data.find('div', class_='collapsible results').find_all('div',class_='item')
###hemisphere_results


# In[19]:


# Loop through hemisphere results
for each_hemisphere in hemisphere_results:
    
    # Get each hemisphere title 
    # hem_title = each_hemisphere.find('div', class_='description').h3.text
    hem_title = each_hemisphere.find('div', class_='description').find('a', class_='itemLink product-item').h3.text
    ###print(hem_title)
    # Exclude the word 'Enhanced'
    short_hem_title = ' '.join(hem_title.split()[0:-1])
    ###print(short_hem_title)
     
    # Get each hemisphere image URL
    base_hem_url = 'https://astrogeology.usgs.gov'

    each_hem_image_url = base_hem_url + each_hemisphere.find('a',class_='itemLink product-item')['href']
    ###print(each_hem_image_url)
    
    browser.visit(each_hem_image_url)
    time.sleep(2)
    each_hem_img_html = browser.html
    each_hem_data = BeautifulSoup(each_hem_img_html, 'html.parser')
    full_image_url = each_hem_data.find('div',class_='downloads').a['href']
    ###print(full_image_url)
    
    each_hemisphere_image = {
        "title" : short_hem_title,
        "image_url" : full_image_url
    }
    print(each_hemisphere_image)
    # Append each hemisphere info to the list of all hemipheres  
    hemisphere_image_urls.append(each_hemisphere_image)


# In[20]:


###print(hemisphere_image_urls)

