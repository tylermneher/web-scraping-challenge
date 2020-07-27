from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd


def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()

    browser.visit('https://mars.nasa.gov/news/')

    time.sleep(1)

    html = browser.html
    soup = bs(html, "html.parser")

    title_results = soup.find_all('div', class_='content_title')
    news_title = title_results[0].text

    p_results = soup.find_all('div', class_='article_teaser_body')
    news_p = p_results[0].text


    
    browser.visit('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')

    time.sleep(1)

    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(2)
    browser.click_link_by_partial_text('more info')

    html = browser.html
    soup = bs(html, 'html.parser')

    results = soup.find_all('figure', class_='lede')
    relative_img_path = results[0].a['href']
    featured_img = 'https://www.jpl.nasa.gov' + relative_img_path



    browser.visit('https://twitter.com/marswxreport?lang=en')
    
    time.sleep(1)
    
    html = browser.html
    soup = bs(html, 'html.parser')

    results = soup.find_all('p', class_="TweetTextSize")

    mars_weather = results[0].text
    

    tables = pd.read_html('https://space-facts.com/mars/')

    df = tables[1]

    df.columns=['description', 'value']
    
    mars_facts_table = df.to_html(classes='data table', index=False, header=False, border=0)



    browser.visit('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars')
    
    time.sleep(1)
    
    html = browser.html
    soup = bs(html, 'html.parser')

    hemi_names = []

    results = soup.find_all('div', class_="collapsible results")
    hemispheres = results[0].find_all('h3')

    for name in hemispheres:
        hemi_names.append(name.text)

    thumbnail_results = results[0].find_all('a')
    thumbnail_links = []

    for thumbnail in thumbnail_results:
        
   
        if (thumbnail.img):
            
            thumbnail_url = 'https://astrogeology.usgs.gov/' + thumbnail['href']
            
            thumbnail_links.append(thumbnail_url)
    
    full_imgs = []

    for url in thumbnail_links:
        
        browser.visit(url)
        
        html = browser.html
        soup = bs(html, 'html.parser')
        
        results = soup.find_all('img', class_='wide-image')
        relative_img_path = results[0]['src']
        
        img_link = 'https://astrogeology.usgs.gov/' + relative_img_path
        
        full_imgs.append(img_link)

    mars_hemi_zip = zip(hemi_names, full_imgs)

    hemisphere_image_urls = []

    for title, img in mars_hemi_zip:
        
        mars_hemi_dict = {}
        
        mars_hemi_dict['title'] = title
        
        mars_hemi_dict['img_url'] = img
        
        hemisphere_image_urls.append(mars_hemi_dict)
    

    mars_data = {
        "news_title": news_title,
        "news_paragraph": news_p,
        "featured_image": featured_img,
        "weather": mars_weather,
        "mars_facts": mars_facts_table,
        "hemispheres": hemisphere_image_urls
    }

    browser.quit()

    return mars_data