from typing import List, Dict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import re

class Scraper:
    def __init__(self,driver: webdriver.Chrome, base_url: str, page_number: int, product_container_locator: str, product_title: str,product_price: str,product_image: str,wait_time: int = 5):
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
        # the main function for getting data and appending to dictionary
        for page in range(1, self.page_number + 1):
            url = f"{self.base_url}{page}"
            self.driver.get(url)
            product_container = self.driver.find_elements(By.XPATH, self.product_container_locator)
            products = []
            for product in product_container:
                title, weight = self.get_product_title(product)
                title = self.clean_product_title(title)
                print("Cleaned: " + title)
                img_url = self.get_product_image_url(product)
                price = self.get_product_price(product)
                product_data = {
                    "title": title,
                    "img_url": img_url,
                    "price": price,
                    "weight": weight
                }
                products.append(product_data)
            self.data.extend(products)

    # def clean_product_title(self, title: str) -> str:
    #     title = title.replace('Tesco', '').strip()
    #     weight_idx = title.rfind(' ')
    #     if weight_idx != -1:
    #         title = title[:weight_idx]
    #     return title
    
    def get_product_weight(self, title: str) -> str:
        title = title.strip()
        weight_idx = title.rfind(' ')
        if weight_idx != -1:
            weight = title[weight_idx+1:].strip().rstrip('0123456789 .')
            return weight
        return None
    
    def clean_product_title(self, title: str) -> str:
        title = re.sub(r'Tesco\s+','',title)
        title = re.sub(r'\d+G\s*\+*','',title)
        return title.strip()

    def get_product_title(self, product: WebElement) -> str:
        title_locator = (By.XPATH, self.product_title)
        title_element = self.wait.until(EC.visibility_of_element_located(title_locator))
        print("Unclean: " + title_element.text)
        title = title_element.text.strip()
        weight = self.get_product_weight(title)
        title = self.clean_product_title(title)
        return title, weight

    def get_product_image_url(self, product: WebElement) -> str:
        image_locator = (By.XPATH, self.product_image)
        image = self.wait.until(EC.visibility_of_element_located(image_locator))
        return image.get_attribute('srcset').split(',')[0].replace(' 768w','')

    def get_product_price(self, product: WebElement) -> str:
        price_locator = (By.XPATH, self.product_price)
        try:
            price = self.wait.until(EC.visibility_of_element_located(price_locator))
            price = price.text
        except:
            price = "Out of Stock"
        return price.replace("u00a3", "£")

    def write_to_file(self, file_path: str):
        with open(file_path, 'w') as file:
            json.dump(self.data, file)
        

if __name__ == '__main__':
    driver = webdriver.Chrome()
    
    with open('src/market_scrapers/website_details.json') as f:
        xpath_data = json.load(f)
    
    tesco_scraper = Scraper(
        driver = driver,
        base_url = xpath_data['tesco']['base_url'],
        page_number = 1,
        product_container_locator = xpath_data['tesco']['product_container'],
        product_title = xpath_data['tesco']['product_title'],
        product_price = xpath_data['tesco']['product_price'],
        product_image = xpath_data['tesco']['product_image']
    )
    tesco_scraper.scrape()
    tesco_scraper.write_to_file('src/scraped_data/tesco_data7.json')
    driver.quit()