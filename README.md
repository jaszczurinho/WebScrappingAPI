# Web Scraping App for RBC.ru webpage

This repository contains a Flask web application for web scraping articles from <a href='https://www.rbc.ru/'>RBC.ru</a> based on user search queries. The app utilizes Selenium and SeleniumWire for web scraping and provides a simple web interface for users to input keywords and retrieve relevant articles.

## Features
- **Proxy Configuration:** Configures a proxy for web scraping, enhancing privacy and bypassing potential restrictions.
  
- **Web Scraping:** Utilizes Selenium and SeleniumWire to scrape articles from RBC.ru based on user search queries.

- **Multiprocessing:** Employs the multiprocessing module to enhance the efficiency of web scraping multiple pages simultaneously.

  


## How to Run the App

1. Ensure you have Python installed on your system.
2. Install the required dependencies using pip: `pip install -r requirements.txt`.
3. Run the Python script `app.py` to start the Flask web application.
4. Access the web interface by navigating to [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in your web browser.
5. Enter keywords in the search form and submit to retrieve relevant article data.

## Dependencies

- Flask
- Selenium
- SeleniumWire
- Chromedriver
- Webdriver Manager
- Multiprocessing

Install the dependencies using:

```bash
pip install -r requirements.txt
