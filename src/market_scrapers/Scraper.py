import time
from typing import List, Dict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urljoin
import json

class Scraper:
    def __init__(self, driver: webdriver.Chrome, base_url: str, page_number: int, product_container_locator: str, product_title: str,product_price: str,product_image: str,wait_time: int = 6):
        self.driver = driver
        self.base_url = base_url
        self.page_number = page_number
        self.product_container_locator = product_container_locator
        self.product_title = product_title
        self.product_price = product_price
        self.product_image = product_image
        self.wait_time = wait_time
        self.wait = WebDriverWait(self.driver, self.wait_time)
        self.data = []

    def scrape(self):
        # If the webpage holds all product in one page
        if self.page_number == 1:
            url = f"{self.base_url}"
            self.driver.get(url)
            product_container = self.driver.find_elements(By.XPATH, self.product_container_locator)
            products = []
            for product in product_container:
                title = self.get_product_title_attribute(product)
                img_url = self.get_product_image_url(product)
                price = self.get_product_price(product)
                product_data = {
                    "title": title,
                    "img_url": urljoin(self.base_url, img_url),
                    "price": price,
                }
                products.append(product_data)
            self.data.extend(products)
        else: # If the webpage has multiple pages for the products
            for page in range(1, self.page_number + 1):
                url = f"{self.base_url}{page}"
                self.driver.get(url)
                product_container = self.driver.find_elements(By.XPATH, self.product_container_locator)
                products = []
                for product in product_container:
                    title = self.get_product_title(product)
                    img_url = self.get_product_image_url(product)
                    price = self.get_product_price(product)
                    product_data = {
                        "title": title,
                        "img_url": img_url,
                        "price": price,
                    }
                    products.append(product_data)
                self.data.extend(products)

    # WILL COME BACK TO THIS FOR LATER FORMATTING
    # def get_product_weight(self, title: str) -> str:
    #     title = title.strip()
    #     weight_idx = title.rfind(' ')
    #     if weight_idx != -1:
    #         weight = title[weight_idx+1:].strip().rstrip('0123456789 .')
    #         return weight
    #     return None
    
    # def clean_product_title(self, title: str) -> str:
    #     title = re.sub(r'Tesco\s+','',title)
    #     title = re.sub(r'\d+G\s*\+*','',title)
    #     return title.strip()

    def get_product_title(self, product: WebElement) -> str:
        title_locator = (By.XPATH, self.product_title)
        title = product.find_element(*title_locator)
        title = title.text.strip()
        return title
    def get_product_title_attribute(self,product: WebElement) -> str:
        print(self.product_title)
        WebDriverWait(self.driver,2)
        title_locator = (By.XPATH,self.product_title)
        title_ele = product.find_element(*title_locator)
        title = title_ele.get_attribute('title')
        title = title.strip()
        print(title)
        return title

    def get_product_image_url(self, product: WebElement) -> str:
        image_locator = (By.XPATH, self.product_image)
        image = self.wait.until(EC.visibility_of_element_located(image_locator))
        # image = image.get_attribute('srcset').split(',')[0].replace(' 1x','')
        return image.get_attribute('srcset').split(',')[0].replace(' 768w','')

    def get_product_price(self, product: WebElement) -> str:
        price_locator = (By.XPATH, self.product_price)
        try:
            price_element = self.wait.until(EC.visibility_of_element_located(price_locator))
            price_text = price_element.text
            price_en = price_text.encode("ascii","ignore")
            price = price_en.decode()
        except:
            price = "Out of Stock"
        return price

    def write_to_file(self, file_path: str):
        with open(file_path, 'w') as file:
            json.dump(self.data, file)

if __name__ == '__main__':
    driver = webdriver.Chrome()
    
    with open('src/market_scrapers/website_details.json') as f:
        xpath_data = json.load(f)
    
    # Scrape Tesco
    # tesco_scraper = Scraper(
    #     driver = driver,
    #     base_url = xpath_data['tesco']['base_url'],
    #     page_number = 154,
    #     product_container_locator = xpath_data['tesco']['product_container'],
    #     product_title = xpath_data['tesco']['product_title'],
    #     product_price = xpath_data['tesco']['product_price'],
    #     product_image = xpath_data['tesco']['product_image']
    # )
    # tesco_scraper.scrape()
    # tesco_scraper.write_to_file('src/scraped_data/tesco_data.json')
    
    # Scrape Morrison
    morrison_scraper = Scraper(
        driver = driver,
        base_url = xpath_data['morrisons']['base_url'],
        page_number = 1,
        product_container_locator = xpath_data['morrisons']['product_container'],
        product_title = xpath_data['morrisons']['product_title'],
        product_price = xpath_data['morrisons']['product_price'],
        product_image = xpath_data['morrisons']['product_image']
    )
    morrison_scraper.scrape()
    morrison_scraper.write_to_file('src/scraped_data/morrison_data3.json')
    
    driver.quit()