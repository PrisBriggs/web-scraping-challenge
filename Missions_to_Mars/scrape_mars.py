# Dependencies
import json
import pandas as pd
import requests
import pymongo
import time

from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager


def init_browser():
    # Path to the chromedriver
    executable_path = {'executable_path': ChromeDriverManager().install()}
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

# Step 1 - Scraping
# NASA Mars News

def scrape():
    browser = init_browser()
    
    # create mars_data dict that we can insert into mongo
    mars_data = {}

    # Have the browser navigate to the webpage and copy the content
    # URL for NASA Mars News
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    
    time.sleep(1)
    
    # Extract the title of the HTML document
    doc_title = soup.title.text.strip()
    
    # Find the title related to the latest News
    try: 
        latest_news_title = soup.find('div', class_='content_title')
        news_title = latest_news_title.text.strip()
    except:
        news_title = "web scraping not working"


    # Find the paragraph text related to the latest News
    try:
        latest_news_p = soup.find('div', class_='article_teaser_body')
        news_p = latest_news_p.text.strip()
    except:
        news_p = "web scraping not working"

    time.sleep(1)
    
    # JPL Mars Space Images - Featured Image
    # Have the browser navigate to the webpage and copy the content
    # URL for JPL Mars Space Images - Featured Image
    url1 = 'https://spaceimages-mars.com'
    browser.visit(url1)
    html1 = browser.html
    soup1 = bs(html1, 'html.parser')
    
    # Find the featured image
    img = soup1.find('img', class_='headerimage fade-in').get('src')
    featured_image = ['https://spaceimages-mars.com/' + img]
    featured_image_url = (featured_image[0])

    time.sleep(1)

    # Mars Facts
    # URL for Mars Facts
    url2 = 'https://galaxyfacts-mars.com'

    # Use Pandas to automatically scrape the tabular data from the page.
    table = pd.read_html(url2)
    
    # Transform table in dataframe.
    df = table[0]
    df.head()

    # Convert data to html table string.
    html_table = df.to_html()
    
    # Strip unwanted newlines to clean up the table.
    html_table.replace('\n', '')
    html_table

    time.sleep(1)

    mars_data = {
        "Latest news title: ": news_title,
        "Latest news paragraph: ": news_p,
        "Feature Image URL: ": featured_image_url,
        "Mars Facts table: ": html_table        
    }

    # Quit browser
    browser.quit()
    
    return mars_data




