# Web Scraper: NASA / Mars Data
This project scrapes data from various websites. While some of this could be done using `requests` package in python, `splinter` is the main tool since some web pages were missing elements when `requests` was used. 

![GitHub language count](https://img.shields.io/github/languages/count/CCom20/web-scraping-challenge?style=for-the-badge)

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

    mars_data['news_title'] = news_title
    mars_data['news_para'] = news_para

Since there are two other processes that need to use `splinter`, the browser is kept open until all data is collected. 

## JPL Mars Space Image

Here we're only interested in grabbing the url for the image, not working directly with the image or downloading it. 

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    html = browser.html
    soup_jpl = bs(html, 'html.parser')

    featured_img = soup_jpl.find_all(name='a', class_='button fancybox')[0].get('data-fancybox-href')

    mars_data["jpl_img"] = f'https://www.jpl.nasa.gov{featured_img}'

As with the previous section, each piece of information we want is added to a dictionary. At the end, all of this will be added to a Mongo database.

## Mars Hemispheres

After visiting the USGS website, we select the hyperlinks that match the desired text. This is mainly done in a `for` loop, wherein the image title and the image url are saved as key-value pairs in a list (i.e., a list of dictionaries). 

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

As you might note, since this is the last web scraping we need to do, the browser is then closed. In `insert_data.py`, we connect to MongoDB and update the database with the information; and `app.py` serves this to the user with the option to scrape again. The button to scrape mars reinitiates the scrape function. 
