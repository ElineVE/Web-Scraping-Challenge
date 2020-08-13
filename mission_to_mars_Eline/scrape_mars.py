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


    mars = {}

    # executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome')




    # URL of page to be scraped

    news_url = 'https://mars.nasa.gov/mars2020/news/'

    # Retrieve page with the requests module
    news_response = requests.get(news_url)
    # browser.visit(news_url)
    
    # Create BeautifulSoup object; parse with 'html'
    soup = bs(browser.html, "html.parser")




    # Scrape the latest News Title and Paragraph Text
    news_title = soup.find("div", class_='listTextLabel').find('h2', class_='alt01').text.strip()
    news_p = soup.find("div", class_='listTextLabel').find('p').text.strip()
    # news_href = soup.find("h2", class_='alt01').a["href"]
    # news_source_url = news_url
    print(news_title)
    print(news_p)
    # print(news_href)
    # print(f'Source: {news_source_url}')
    mars["news_title"] = news_title
    mars["news_p"] = news_p


   


    # Add url provided, create variable "featured_image_url", open browser

    featured_image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

    browser.visit(featured_image_url)




    html_image = browser.html

    soup = bs(html_image, 'html.parser')





    featured_image_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

    main_url = 'https://www.jpl.nasa.gov'

    featured_image_url = main_url + featured_image_url

    featured_image_url

    mars["featured_image_url"] = featured_image_url
    mars




    facts_url = 'https://space-facts.com/mars/'
    mars_facts = pd.read_html(facts_url)

    mars_df = mars_facts[0]

    mars_df




    mars_df.rename(columns={0 : "Attribute", 1 : "Value"}).set_index(["Attribute"])




    mars_df.to_html()
    mars["facts"]=mars_df.to_html()
    mars


    

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
  


    mars["hemisphere"]=hemisphere_image_urls



    print(mars)
    return mars

if __name__ == "__main__":
    print(scrape_all())
    