from urllib.parse import urljoin
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC


class Scraper:
    def __init__(self, driver: webdriver.Chrome, base_url: str, page_number: int, product_container_locator: str,
                 product_title: str, product_price: str, product_image: str, wait_time: int = 6):
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
        else:  # If the webpage has multiple pages for the products
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

    def get_product_title(self, product: webdriver.remote.webelement.WebElement) -> str:
        title_locator = (By.XPATH, self.product_title)
        title = product.find_element(*title_locator)
        title = title.text.strip()
        return title

    def get_product_title_attribute(self, product: WebElement) -> str:
        title_locator = (By.XPATH, self.product_title)
        title_element = self.wait.until(EC.visibility_of_element_located(title_locator))
        title = title_element.get_attribute('title').strip()
        return title
    
    def get_product_price(self, product: WebElement) -> str:
        price_locator = (By.XPATH, self.product_price)
        try:
            price_element = self.wait.until(EC.visibility_of_element_located((price_locator[0], f"{price_locator[1]}[ancestor::div[@class='item-content']]")))
            price_text = price_element.text
            price_en = price_text.encode("ascii", "ignore")
            price = price_en.decode()
        except:
            price = "Out of Stock"
        return price


