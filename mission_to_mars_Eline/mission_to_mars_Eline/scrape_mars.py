#!/usr/bin/env python
# coding: utf-8



#import dependencies
from bs4 import BeautifulSoup as bs
import requests
import pymongo
import time
from splinter import Browser
import pandas as pd


def scrape_all(): 

    #Splinter Windows work-around for chromedriver.exe 'e' error
    # from webdriver_manager.chrome import ChromeDriverManager
    # executable_path = {'executable_path': ChromeDriverManager().install()}

    #Splinter browser setup for MacOS
    # executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome')


    mars = {}

    # Getting the Latest News Title

    url = 'https://mars.nasa.gov/news/'

    browser.visit(url)

    html = browser.html

    soup = bs(html, 'html.parser')

    news_title = soup.find_all('div', class_='content_title')[1].get_text()

    mars["news_title"] = news_title

    print(news_title)




    # Getting the Paragraph

    news_p = soup.find('div', class_='article_teaser_body').get_text()
    mars["news_paragraph"] = news_p
    print(news_p)




    # Printing Title and Paragraph like example

    # print(f"Title:\n\n{news_title}")
    # print("\n----------------------------------------------------------\n")
    # print(f"Paragraph:\n\n{news_p}")




    # Add url provided, create variable "featured_image_url", open browser

    featured_image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

    browser.visit(featured_image_url)




    html_image = browser.html

    soup = bs(html_image, 'html.parser')




    featured_image_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

    main_url = 'https://www.jpl.nasa.gov'

    featured_image_url = main_url + featured_image_url

    featured_image_url

    mars["featured_image"] = featured_image_url


    browser.quit()




    facts_url = 'https://space-facts.com/mars/'

    # browser.visit(facts_url)




    mars_facts = pd.read_html(facts_url)

    mars_df = mars_facts[0]

    mars_df




    mars_df.rename(columns={0 : "Attribute", 1 : "Value"}).set_index(["Attribute"])



    mars_df.columns = ['Attribute','Value']

    mars_df = mars_df.rename(columns={0 : "Attribute", 1 : "Value"}).set_index(["Attribute"])

    mars_df = mars_df.to_html()
    

    mars["facts"] = mars_df

    # data = mars_df.to_dict(orient='records')

    mars_df




    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(hemispheres_url)




    hemisphere_image_urls = []

    links = browser.find_by_css("a.product-item h3")

    for x in range(len(links)):
        hemisphere = {}
        browser.find_by_css("a.product-item h3")[x].click()
        sample_element = browser.links.find_by_text('Sample').first
        hemisphere["img_url"] = sample_element['href']
        hemisphere["title"] = browser.find_by_css("h2.title").text
        hemisphere_image_urls.append(hemisphere)
        browser.back()
        



    hemisphere_image_urls

    mars["hemisphere"] = hemisphere_image_urls
    return mars
if __name__ == "__main__":
    print(scrape_all())














