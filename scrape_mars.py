from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

news_url = 'https://redplanetscience.com/'
feature_url = 'https://spaceimages-mars.com/'
facts_url = 'https://galaxyfacts-mars.com/'
astro_geo_url = 'https://marshemispheres.com/'



def scrape():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    #visit news site
    browser.visit(news_url)

    time.sleep(1)


    html = browser.html
    soup = bs(html, 'lxml')

    # find and save title and content of first article
    news_title = soup.find('div', class_="content_title").get_text()
    news_p = soup.find('div', class_='article_teaser_body').get_text()
    

    # visit image site
    browser.visit(feature_url)

    time.sleep(1)


    # find and save link to feature image
    feature_image = browser.links.find_by_partial_href('feature').first['href']
    
    # visit geological site
    browser.visit(astro_geo_url)

    time.sleep(1)

    # find all links to image sites
    image_links = browser.find_by_css('.product-item').links.find_by_partial_text('Enhance')

    # create list of urls
    listoflinks = []
    for i in range(4):
        listoflinks.append(image_links[i]['href'])


    # visit urls and find and save jpeg images
    imglist = []
    for i in listoflinks:
        browser.visit(i)
        img = browser.links.find_by_text('Sample')
        name = browser.find_by_css('.title').first.value.rstrip('Enhanced').strip()
        dic = {}
        dic['title'] = name
        dic['img_url'] = img['href']
        
        imglist.append(dic)


    # pandas scrape comparison table
    tables = pd.read_html(facts_url)
    df = tables[0]
    df.rename(columns=df.iloc[0], inplace=True)
    df.drop([0], inplace=True)
    df.set_index(['Mars - Earth Comparison'], inplace=True)
    # save at html table
    html_table = df.to_html(index=True, classes=["table", "table-striped", "table-bordered"])


    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "feature_image": feature_image,
        "hemispheres": imglist,
        "data_table": html_table
    }

    browser.quit()

    # Return results
    return mars_data