from typing import List, Dict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

class Scraper:
    def __init__(self, base_url: str, page_number: int, product_container_locator: str, wait_time: int = 5):
        self.base_url = base_url
        self.page_number = page_number
        self.product_container_locator = product_container_locator
        self.wait_time = wait_time
        self.wait = WebDriverWait(self.driver, self.wait_time)
        self.data = []

    def scrape(self):
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
        title_locator = (By.XPATH, ".//a[@class='styled__Anchor-sc-1xbujuz-0 csVOnh beans-link__anchor']//span[@class='styled__Text-sc-1xbujuz-1 ldbwMG beans-link__text']")
        title = self.wait.until(EC.visibility_of_element_located(title_locator))
        return title.text

    def get_product_image_url(self, product: WebElement) -> str:
        image_locator = (By.XPATH, ".//div[@class='product-image__container']//img")
        image = self.wait.until(EC.visibility_of_element_located(image_locator))
        return image.get_attribute('srcset').split(',')[0].replace(' 768w','')

    def get_product_price(self, product: WebElement) -> str:
        price_locator = (By.XPATH, ".//p[@class='styled__StyledHeading-sc-119w3hf-2 jWPEtj styled__Text-sc-8qlq5b-1 lnaeiZ beans-price__text']")
        try:
            price = self.wait.until(EC.visibility_of_element_located(price_locator))
        except:
            price = "Out of Stock"
        return price.text

    def write_to_file(self, file_path: str):
        with open(file_path, 'w') as file:
            json.dump(self.data, file)

if __name__ == '__main__':
    driver = webdriver.Chrome()
    scraper = Scraper(
        base_url = "https://www.tesco.com/groceries/en-GB/shop/fresh-food/all?page=",
        page_number = 2,
        product_container_locator = "//li[contains(@class, 'product-list--list-item')]"
    )
    scraper.scrape()
    scraper.write_to_file('src/scraped_data/tesco_data.json')
    driver.quit()