# scrape.py - webscraping of several mars news websites for the latest mars news
# author: Inna Baloyan

# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import time
import datetime as dt


# Initialize return dictionary
mars_news_data = {}

# Main module, will be called by Flask app
def scrape_all_sites():

    # Initialize chrome browser and pass it to other functions
    browser = Browser("chrome", executable_path="chromedriver", headless=True)

    news_title, news_text = get_mars_news(browser)

    # Run all scraping functions and store all mars_news_data in this dictionary
    mars_news_data = {
        "news_title": news_title,
        "news_text": news_text,
        "featured_image_url": get_featured_space_image(browser), 
        "mars_weather": get_mars_weather(browser),
        "mars_facts": get_mars_facts(),
        "hem_image_urls": get_hemisphere_urls(browser),  
        "last_modified": dt.datetime.utcnow()    
    }

    # Quit browser and return all needed data
    browser.quit()

    return mars_news_data



# Web Scraping
# Nasa Mars News scraping function
def get_mars_news(browser):

    # URL of NASA Mars site, News page to be scraped
    mars_url = 'https://mars.nasa.gov/news/'
    browser.visit(mars_url)
    time.sleep(1)

    # Get HTML page with the browser; create BeautifulSoup object; parse with 'html.parser'
    mars_html = browser.html
    mars_nasa_data = BeautifulSoup(mars_html, 'html.parser')

    # Get needed fields from html page, wait a second
    # browser.is_element_present_by_css("ul.item_list li.slide",wait_time=1)

    # Extract the first news title and description
    # Get news_title and news_teaser_body
    try:
        ###article_element = mars_nasa_data.select_one("ul.item_list li.slide")
        ###print(f"The article_element is: {article_element}") 
    
        ###news_title = article_element.find("div", class_="content_title").get_text()
        news_title = mars_nasa_data.find('ul', class_="item_list").find('li',class_="slide").find('div',class_="content_title").text
        ###print(f"The news_title is: {news_title}") 
    
        ###news_teaser_body = article_element.find("div", class_="article_teaser_body").get_text()
        news_teaser_body = mars_nasa_data.find('ul',class_="item_list").find('li',class_="slide").find('div',class_="article_teaser_body").text
        ###print(f"The news teaser body is: {news_teaser_body}")
    
    except AttributeError as e:
        print(e)

    return news_title, news_teaser_body    

# Featured Space Image scraping function
def get_featured_space_image(browser):
 
    # URL of NASA Mars site, JPL Featured Space Images page to be scraped
    mar_space_images_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(mar_space_images_url)

    # Find and Click "FULL IMAGE" button
    full_image_data = browser.find_by_id('full_image')
    full_image_data.click()

    # Find and Click 'more info' button, wait a second
    ### browser.is_element_present_by_text('more info',wait_time=1)
    time.sleep(1)
    more_info_data = browser.find_link_by_partial_text('more info')
    more_info_data.click()

    # Get HTML page with the browser; create BeautifulSoup object; parse with 'html.parser'
    time.sleep(1)
    mars_images_html = browser.html
    mars_images_data = BeautifulSoup(mars_images_html, 'html.parser')

    # Get featured_image_url
    try:    
        featured_image_url = mars_images_data.find('figure', class_='lede').a['href']
        ###print(f"The featured_image_url is: {featured_image_url}") 
    
    except AttributeError:
        return None

    # Compose complete url string for this full size image png
    full_image_url = "https://www.jpl.nasa.gov" + featured_image_url
    ###print(f"The full_image_url is: {full_image_url}") 

    return full_image_url


# Mars Weather scraping from Twitter function
def get_mars_weather(browser):

    # # Initialize chrome browser
    # browser = init_browser()
    
    # URL of Mars Weather twitter page to be scraped
    mars_twitter_weather_url = 'https://twitter.com/marswxreport?lang=en)'
    browser.visit(mars_twitter_weather_url)

    # Get HTML page with the browser; create BeautifulSoup object; parse with 'html.parser'
    mars_weather_html = browser.html
    mars_weather_data = BeautifulSoup(mars_weather_html, 'html.parser')

    # Scrape the latest Mars Weather tweet text
    mars_weather  = mars_weather_data.find('div', attrs={"class": "tweet", "data-name": "Mars Weather"}).find('p',class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    ###print(f"The mars_weather is: {mars_weather}") 

    return mars_weather

# Mars Facts scraping into HTML table
# Read Mars Facts webpage; use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
def get_mars_facts():

    mars_facts_url = 'https://space-facts.com/mars/'
    mars_facts_table_df = pd.read_html(mars_facts_url)[0]
    mars_facts_table_df.columns = ['Description','Value']
    mars_facts_table_df.set_index('Description', inplace=True)
    mars_facts_table_df

    # Use Pandas to convert the data to a HTML table string
    ####mars_facts_table_df.to_html('MarsFactsTable.html', index=False )
    mars_facts_table_df.to_html()

    return mars_facts_table_df.to_html()
    # Format HTML table with bootstrap
    ###return mars_facts_table_df.to_html(classes="table table-striped")

# Mars Hemispheres - URL of USGS Astrogeology site to be scraped
# to obtain high resolution images for each of Mar's hemispheres
def get_hemisphere_urls(browser):

    # # Initialize chrome broowser
    # browser = init_browser()

    # URL of USGS Astrogeology site
    usgs_astrogeology_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(usgs_astrogeology_url)

    # Initialize the list for the dictionary of hemisphere images 
    hemisphere_image_urls = []

    # Get HTML page with the browser; create BeautifulSoup object; parse with 'html.parser'
    usgs_astrogeology_html = browser.html
    all_hemisphere_data = BeautifulSoup(usgs_astrogeology_html, 'html.parser')

    # Get the iterable list of all hemispere information
    hemisphere_results = all_hemisphere_data.find('div', class_='collapsible results').find_all('div',class_='item')

    # Loop through hemisphere results
    for each_hemisphere in hemisphere_results:
    
        # Get each hemisphere title 
        # hem_title = each_hemisphere.find('div', class_='description').h3.text
        hem_title = each_hemisphere.find('div', class_='description').find('a', class_='itemLink product-item').h3.text
   
        # Exclude the word 'Enhanced'
        short_hem_title = ' '.join(hem_title.split()[0:-1])
     
        # Get each hemisphere image URL
        base_hem_url = 'https://astrogeology.usgs.gov'

        each_hem_image_url = base_hem_url + each_hemisphere.find('a',class_='itemLink product-item')['href']
        ###print(each_hem_image_url)
    
        browser.visit(each_hem_image_url)
        time.sleep(1)
        each_hem_img_html = browser.html
        each_hem_data = BeautifulSoup(each_hem_img_html, 'html.parser')
        full_image_url = each_hem_data.find('div',class_='downloads').a['href']
        ###print(full_image_url)
    
        each_hemisphere_image = {
            "title" : short_hem_title,
            "image_url" : full_image_url
        }
        ###print(each_hemisphere_image)
        
        # Append each hemisphere info to the list of all hemipheres  
        hemisphere_image_urls.append(each_hemisphere_image)
        ###print(hemisphere_image_urls)

        # Navigate back
        browser.back()

    return hemisphere_image_urls



if __name__ == "__main__":
    
    # If run from shell
    print (scrape_all_sites())