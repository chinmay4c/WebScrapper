import time
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup Chrome driver with options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run headless for faster scraping
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Function to scrape data from Amazon
def scrape_amazon(query):
    amazon_url = f"https://www.amazon.in/s?k={query}"
    driver.get(amazon_url)
    
    # Wait until the products are loaded
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-component-type="s-search-result"]')))
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    products = soup.find_all('div', {'data-component-type': 's-search-result'})
    
    amazon_data = []
    for product in products:
        title = product.h2.text.strip()
        try:
            price = product.find('span', 'a-price-whole').text.strip()
        except AttributeError:
            price = "Price not available"
        amazon_data.append({'Title': title, 'Price': price})
    
    return amazon_data

# Function to scrape data from Flipkart
def scrape_flipkart(query):
    flipkart_url = f"https://www.flipkart.com/search?q={query}"
    driver.get(flipkart_url)
    
    # Wait until the products are loaded
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, '_2kHMtA')))
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    products = soup.find_all('div', {'class': '_2kHMtA'})
    
    flipkart_data = []
    for product in products:
        title = product.find('a', {'class': 'IRpwTa'}).text.strip()
        try:
            price = product.find('div', {'class': '_30jeq3 _1_WHN1'}).text.strip()
        except AttributeError:
            price = "Price not available"
        flipkart_data.append({'Title': title, 'Price': price})
    
    return flipkart_data

# Function to scrape data from Myntra
def scrape_myntra(query):
    myntra_url = f"https://www.myntra.com/{query}"
    driver.get(myntra_url)
    
    # Wait until the products are loaded
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'product-base')))
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    products = soup.find_all('li', {'class': 'product-base'})
    
    myntra_data = []
    for product in products:
        title = product.find('h3', {'class': 'product-brand'}).text.strip()
        try:
            price = product.find('div', {'class': 'product-price'}).text.strip()
        except AttributeError:
            price = "Price not available"
        myntra_data.append({'Title': title, 'Price': price})
    
    return myntra_data

# Function to save data to a CSV file
def save_to_csv(data, filename):
    keys = data[0].keys()
    with open(filename, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)

# Example usage
query = 'laptop'
amazon_data = scrape_amazon(query)
flipkart_data = scrape_flipkart(query)
myntra_data = scrape_myntra('t-shirt')  # Different query for Myntra

# Save data to CSV files
save_to_csv(amazon_data, 'amazon_products.csv')
save_to_csv(flipkart_data, 'flipkart_products.csv')
save_to_csv(myntra_data, 'myntra_products.csv')

# Close the driver
driver.quit()

print("Scraping complete. Data saved to CSV files.")
