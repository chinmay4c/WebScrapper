from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Setup Chrome driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Function to scrape data from Amazon
def scrape_amazon(query):
    amazon_url = f"https://www.amazon.in/s?k={query}"
    driver.get(amazon_url)
    time.sleep(2)
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    products = soup.find_all('div', {'data-component-type': 's-search-result'})
    
    for product in products:
        title = product.h2.text.strip()
        try:
            price = product.find('span', 'a-price-whole').text.strip()
        except AttributeError:
            price = "Price not available"
        print(f"Title: {title}\nPrice: {price}\n")

# Function to scrape data from Flipkart
def scrape_flipkart(query):
    flipkart_url = f"https://www.flipkart.com/search?q={query}"
    driver.get(flipkart_url)
    time.sleep(2)
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    products = soup.find_all('div', {'class': '_2kHMtA'})
    
    for product in products:
        title = product.find('a', {'class': 'IRpwTa'}).text.strip()
        try:
            price = product.find('div', {'class': '_30jeq3 _1_WHN1'}).text.strip()
        except AttributeError:
            price = "Price not available"
        print(f"Title: {title}\nPrice: {price}\n")

# Function to scrape data from Myntra
def scrape_myntra(query):
    myntra_url = f"https://www.myntra.com/{query}"
    driver.get(myntra_url)
    time.sleep(2)
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    products = soup.find_all('li', {'class': 'product-base'})
    
    for product in products:
        title = product.find('h3', {'class': 'product-brand'}).text.strip()
        try:
            price = product.find('div', {'class': 'product-price'}).text.strip()
        except AttributeError:
            price = "Price not available"
        print(f"Title: {title}\nPrice: {price}\n")

# Example usage
scrape_amazon('laptop')
scrape_flipkart('laptop')
scrape_myntra('t-shirt')

# Close the driver
driver.quit()
