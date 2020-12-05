from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import pymongo
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

# Set up Mongo Connection / DB
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

# Recreate DB without Duplicates
mars_db = client.mars_db

# Create Mars_Data Python Dictionary
mars_data = {}

# Function for Scraping Mars Data from Web
def scrape():
    # ------------------------------------------------- #
    # MARS NEWS
    # ------------------------------------------------- #

    # Get response from website
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    mars_news = 'https://mars.nasa.gov/news/'

    browser.visit(mars_news)

    # Set up the text variable 'mars_news_html' 
    mars_news_html = browser.html

    # Set up BeautifulSoup object and print to check
    soup = bs(mars_news_html, 'html.parser')

    # Get the news title and print to make sure it's correct
    news_title = soup.select('div.content_title a')[0].text.strip()

    # Get the news paragraph, print to make sure it's correct
    news_para = soup.select('div.article_teaser_body')[1].text.strip()

    # ---- #
    # ADD TO DICTIONARY #
    # ---- #

    mars_data['news_title'] = news_title
    mars_data['news_para'] = news_para

    # Set URL and open browser
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Get HTML and parse with BeautifulSoup, print to check
    html = browser.html
    soup_jpl = bs(html, 'html.parser')

    # Find Featured Image URL and print to check
    featured_img = soup_jpl.find_all(name='a', class_='button fancybox')[0].get('data-fancybox-href')

    # Visit URL for full-size image
    browser.visit(f'https://www.jpl.nasa.gov{featured_img}')

    # ADD TO DICTIONARY #
    mars_data["jpl_img"] = f'https://www.jpl.nasa.gov{featured_img}'

    # Close Browser
    browser.quit()

    # ------------------------------------------------- #
    # MARS FACTS
    # ------------------------------------------------- #

    # Set URL and Visit
    mars_facts_url = 'https://space-facts.com/mars/'
    mars_df = pd.read_html(mars_facts_url)[0]

    # Export as HTML and save in variable, print to make sure it looks good
    mars_df_html = mars_df.to_html(classes="table")

    # ADD TO DICTIONARY #
    mars_data["mars_facts"] = mars_df_html

    # # ------------------------------------------------- #
    # # MARS HEMISPHERES
    # # ------------------------------------------------- #

    # Start Splinter Again, since we closed the last browser
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit the USGS Astrogeology Site 
    usgs_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(usgs_url)

    # Set HTML for Parsing, then parse with BeautifulSoup
    usgs_html = browser.html
    usgs_soup = bs(usgs_html, 'html.parser')

    # Loop through Links and get info, create dictionary, and append dictionary to list, go back to the first page

    links = usgs_soup.select('a.product-item')

    hemisphere_image_urls = []

    for link in links:
        if link.text != '':
            try:
                browser.links.find_by_partial_text(f'{link.text}').click()
                new_page_html = browser.html
                new_page_soup = bs(new_page_html, 'html.parser')
                img_url = new_page_soup.select('li a')[0].get('href')
                img_dict = {}
                img_dict["title"] = link.text
                img_dict["url"] = img_url
                hemisphere_image_urls.append(img_dict)
                browser.visit(usgs_url)
            except:
                print('Link text not found.')

    browser.quit()

    # ADD TO DICTIONARY #

    mars_data["mars_hemispheres"] = hemisphere_image_urls

    return mars_data