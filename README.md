# Web Scraper: NASA / Mars Data
This project scrapes data from various websites. While some of this could be done using `requests` package in python, `splinter` is the main tool since some web pages were missing elements when `requests` was used. 

## NASA Mars News Scraper
This brief code vitis https://mars.nasa.gov/news/ and gets the latest data. When using `requests`, only July 2020 and eariler articles were returned. Speaking with my peers about why this happens, it was mention `splinter` should be used instead. 

After setting up `splinter`, we grab the html and parse it with BeautifulSoup. We then grab the first news article's title and teaser paragraph:

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    browser.visit(mars_news)

    mars_news = 'https://mars.nasa.gov/news/'

    soup = bs(mars_news_html, 'html.parser')
    
    news_title = soup.select('div.content_title a')[0].text.strip()

    news_para = soup.select('div.article_teaser_body')[1].text.strip()

Since there are two other processes that need to use `splinter`, the browser is kept open until all data is collected. 

## JPL Mars Space Image

Here we're only interested in grabbing the url for the image, not working directly with the image or downloading it. 

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    html = browser.html
    soup_jpl = bs(html, 'html.parser')
