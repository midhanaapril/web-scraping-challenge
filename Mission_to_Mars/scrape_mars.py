from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


def scrape(): 
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)  

    ################################### NASA MARS news site #####################################
    # Visit the Mars news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object
    html = browser.html
    news_soup = soup(html, 'html.parser')

    slide_elem = news_soup.select_one('div.list_text')

    #display the current title content
    results = slide_elem.find('div', class_='content_title')

    # Use the parent element to find the first a tag and save it as `news_title`
    news_title = results.text

    # Use the parent element to find the paragraph text
    results2 = news_soup.find('div', class_='article_teaser_body')
    news_p = results2.text

    ##############################################################################################
    ################################### JPL Space Images Featured Image #####################################
    # Visit URL
    url2 = 'https://spaceimages-mars.com/'
    browser.visit(url2)

    browser.is_element_present_by_css('div.list_text',wait_time =1)
    html2 = browser.html
    img_soup = soup(html2, 'html.parser') 
    full_img = img_soup.find('div',class_='floating_text_area')
    full_img = full_img.find('a')
    full_img = full_img['href']
    
    # find the relative image url
    img_url_rel = full_img

    # Use the base url to create an absolute url
    img_url = url2+img_url_rel

    ##############################################################################################
    ################################### Mars FACTS #####################################

    df = pd.read_html('https://galaxyfacts-mars.com/')
    df = df[0]

    new_head = df.iloc[0]
    df2 = df
    df2.columns = new_head
    df2 = df2.rename(columns={'Mars - Earth Comparison':'Description'})
    df2 = df2.set_index('Description')
    df = df2

    mars_facts = df.to_html()
    

    ##############################################################################################
    ################################### Hemispheres #####################################

    url3 = 'https://marshemispheres.com/'

    browser.visit(url3)
    # Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # Get a list of all of the hemispheres
    links = browser.find_by_css('a.product-item img')

    for i in range(len(links)):
        
        # We have to find the elements on each loop to avoid a stale element exception
        links = browser.find_by_css('a.product-item img')
        links[i].click()
        # Next, we find the Sample image anchor tag and extract the href
        page = browser.html
        hemisphere = soup(page, 'html.parser')
        full_img2 = hemisphere.find('li')
        full_img2 = full_img2.find('a')
        full_img2 = full_img2['href']
        base_url = 'https://marshemispheres.com/'
        full_img2 = base_url+full_img2
        
        # Get Hemisphere title
        title = hemisphere.find('h2')
        title = title.text 
       
        
        # Append hemisphere object to list
        hemisphere_image_urls.append({'img_url':full_img2,'title':title})
        
        # Finally, we navigate backwards
        browser.back()
    
    browser.quit()

    data = {
        'news_title': news_title, 
        'news_p': news_p, 
        'feat_mars_img':img_url, 
        'mars_table':mars_facts,
        'hemisphere':hemisphere_image_urls
        } 

    return data