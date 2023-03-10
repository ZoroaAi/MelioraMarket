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
            counter = 0
            for product in product_container:
                driver.implicitly_wait(10)
                driver.execute_script("window.scrollBy(0,700);")
                title = self.get_product_title(product)
                img_url = self.get_product_image_url(product)
                price = self.get_product_price(product)
                product_data = {
                    "title": title,
                    "img_url": urljoin(self.base_url, img_url),
                    "price": price,
                    "market":"morrisons",
                }
                products.append(product_data)
                counter += 1
                if counter == 300:
                    break
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

    def get_product_title(self, product: WebElement) -> str:
        title_locator = (By.XPATH, self.product_title)
        WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(title_locator))
        title = product.find_element(*title_locator)
        title = title.text.strip()
        print(title)
        return title
    def get_product_title_attribute(self,product: WebElement) -> str:
        print(self.product_title)
        title_locator = (By.XPATH,self.product_title)
        WebDriverWait(product, 10).until(EC.visibility_of_element_located(title_locator))
        title_ele = product.find_element(*title_locator)
        title = title_ele.get_attribute('title')
        title = title.strip()
        return title

    def get_product_image_url(self, product: WebElement) -> str:
        image_locator = (By.XPATH, self.product_image)
        image = product.find_element(*image_locator)
        # image = image.get_attribute('srcset').split(',')[0].replace(' 768w','')
        return image.get_attribute('srcset').split(',')[0].replace(' 1x','')

    def get_product_price(self, product: WebElement) -> str:
        price_locator = (By.CLASS_NAME, self.product_price)
        try:
            price_element = product.find_element(*price_locator)
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
    #     page_number = 155,
    #     product_container_locator = xpath_data['tesco']['product_container'],
    #     product_title = xpath_data['tesco']['product_title'],
    #     product_price = xpath_data['tesco']['product_price'],
    #     product_image = xpath_data['tesco']['product_image']
    # )
    # tesco_scraper.scrape()
    # tesco_scraper.write_to_file('src/scraped_data/tesco_data1111.json')
    
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
    
    
    # /html/body/div[1]/div[1]/div[4]/div[2]/div[2]/ul/li[22]/div[2]/div[1]/a/div[2]/span[1]
    # .//h4[@class='fop-title']/span[1]