#!/usr/bin/env python
# coding: utf-8

# In[1]:


from flask import Flask, request, render_template
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
import json
from multiprocessing import Pool

app = Flask(__name__)

se_options = {
    'proxy': {
        'http': 'http://ulzdszip:3y50iffer98p@45.146.31.101:5688',
        'https': 'https://ulzdszip:3y50iffer98p@45.146.31.101:5688',
        'no_proxy': 'localhost,127.0.0.1'
    }
}

def get_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--ignore-certificate-errors-spki-list')
    chrome_options.add_argument('--ignore-ssl-errors')
    chrome_options.add_argument('--ignore-certificate-errors') 

    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        seleniumwire_options=se_options,
        options=chrome_options
    )

    return driver

def scrape_page(link):
    title = ''
    date = ''
    specific_div = None

    driver = get_driver()
    driver.get(link)

    if 'video' not in link and 'books' not in link and 'autonews' not in link and 'style' not in link and 'companies' not in link:
        if 'style' in link:
            title = driver.find_element(By.XPATH, "//h1[@class='article__header' or @class='article__header__date' | @class='article__header__title']").text
        elif 'life' not in link:
            title = driver.find_element(By.XPATH, "//div[@class='article__header__title'] | //h1[@class='story-header__title'] | //h1[@class= @class='news-detail__title']").text
            if 'pro' not in link:
                try:
                    date = driver.find_element(By.TAG_NAME, 'time').text
                except NoSuchElementException:
                    date = ''
            else:
                date = driver.find_element(By.XPATH, "//div[@class='article__header__title']").text

        if 'life' in link:
            specific_div = driver.find_element(By.TAG_NAME, "article")
        elif 'life' not in link:
            specific_div = driver.find_element(By.XPATH, "//div[@class='article__text article__text_free' or @class='article__text article__text_free js-article-text overflow-visible' or @class='article__text__pro' or @class='article__text__main' or @class='news-detail__content']")
        elif 'prim' in link:
            specific_div = driver.find_element(By.XPATH, '//div[@class="article__text__main"]')

        paragraph_elements = specific_div.find_elements(By.TAG_NAME, 'p')
        paragraphs = [p.text for p in paragraph_elements]

        scraped_data = {
            'title': title,
            'date': date,
            'paragraphs': paragraphs
        }

        driver.quit()
        return scraped_data

    return None

def scrape(search_query):
    url = f'https://www.rbc.ru/search/?query={search_query}'
    driver = get_driver()
    driver.get(url)

    subpages = driver.find_elements(By.XPATH, '//div[@class="search-item__wrap l-col-center"]/a')
    hrefs = [link.get_attribute('href') for link in subpages]

    with Pool() as pool:
        results = pool.map(scrape_page, hrefs)

    scraped_data = [data for data in results if data is not None]

    driver.quit()
    return scraped_data

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        keywords = request.form.get('keywords')
        scraped_data = scrape(keywords)
        scraped_data = json.dumps(scraped_data, ensure_ascii=False)
        return scraped_data

    return render_template('form.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
