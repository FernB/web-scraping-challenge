from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pandas as pd

news_url = 'https://redplanetscience.com/'
feature_url = 'https://spaceimages-mars.com/'
facts_url = 'https://galaxyfacts-mars.com/'
astro_geo_url = 'https://marshemispheres.com/'



def scrape():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit visitcostarica.herokuapp.com
  

    browser.visit(news_url)
    html = browser.html
    soup = bs(html, 'lxml')


    news_title = soup.find('div', class_="content_title").get_text()
    news_p = soup.find('div', class_='article_teaser_body').get_text()
    

    # Scrape page into Soup

    browser.visit(feature_url)
    feature_image = browser.links.find_by_partial_href('feature').first['href']
    # feature_image = feature_image[8:]
    




    browser.visit(astro_geo_url)
    image_links = browser.find_by_css('.product-item').links.find_by_partial_text('Enhance')

    listoflinks = []
    for i in range(4):
        listoflinks.append(image_links[i]['href'])

    # tifflist = {}
    # for i in listoflinks:
    #     browser.visit(i)
    #     tiff = browser.links.find_by_text('Original')
    #     name = browser.find_by_css('.title').first.value.rstrip('Enhanced').strip()
    #     tifflist[name] = tiff['href']

    imglist = []
    for i in listoflinks:
        browser.visit(i)
        img = browser.links.find_by_text('Sample')
        name = browser.find_by_css('.title').first.value.rstrip('Enhanced').strip()
        dic = {}
        dic['title'] = name
        dic['img_url'] = img['href']
        
        imglist.append(dic)


    # tifflist = []
    # for i in listoflinks:
    #     browser.visit(i)
    #     tiff = browser.links.find_by_text('Sample')
    #     name = browser.find_by_css('.title').first.value.rstrip('Enhanced').strip()
    #     dic = {}
    #     dic['title'] = name
    #     dic['img_url'] = tiff['href']
            
    #     tifflist.append(dic)
    



    tables = pd.read_html(facts_url)
    df = tables[0]
    df.rename(columns=df.iloc[0], inplace=True)
    df.drop([0], inplace=True)
    html_table = df.to_html(index=False)







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