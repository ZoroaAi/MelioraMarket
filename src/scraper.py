# from bs4 import BeautifulSoup
# import requests
# from selenium import webdriver

# PATH = "C:\Program Files (x86)\chromedriver.exe"
# driver = webdriver.Chrome(PATH)


# driver.get("https://www.tesco.com/groceries/en-GB/shop/fresh-food/all")

# # Getting element classes of names, prices, and images
# names = driver.find_elements('xpath','//h3[@class="styles__H3-oa5soe-0 bCKNNq"]')
# prices = driver.find_elements('xpath','//div[@class="styled__StyledHeading-sc-119w3hf-2 jWPEtj styled__Text-sc-8qlq5b-1 lnaeiZ beans-price__text"]')
# images = driver.find_elements('xpath','//img[@class="styled__Image-sjvkdn-0 bJErKA product-image beans-responsive-image__image"]')

# #  Extracting the text and URLs of images from elements
# product_names = [name.text for name in names]
# product_prices = [price.text for price in prices]
# product_images = [image.get_attribute('src') for image in images]

# # Store the extracted information
# products = []
# for name, price, image in zip(product_names, product_prices, product_images):
#     product = {
#         'name': name,
#         'price': price,
#         'image': image
#     }
#     products.append(product)

# for i in range(0,5,1):
#     print(products[i])
# 
# 
# driver.close()

import os
import json
from flask import Blueprint, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

scraper = Blueprint('scraper',__name__)

@scraper.route('/groceries')
def get_groceries():
    url = 'https://www.tesco.com/groceries/en-GB/'
    
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode to speed up scraping
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//ul[@class='nav__links']")))
    
    # Wait for the navigation menu to load
    categories = []
    nav_links = driver.find_elements_by_xpath("//ul[@class='nav__links']/li")
    for nav_link in nav_links:
        link_text = nav_link.text
        if link_text.lower() != 'offers':
            category = {'name': link_text, 'products': []}
            nav_link.click()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//ul[@class='product-list grid']/li")))
            # Wait for the product list to load
            product_links = driver.find_elements_by_xpath("//ul[@class='product-list grid']/li//a[@class='product-tile--title']")
            for product_link in product_links:
                product = {'name': product_link.text, 'url': product_link.get_attribute('href')}
                category['products'].append(product)
            categories.append(category)

    driver.quit()
    result = {'categories': categories}
    
    # Save the result to a JSON file
    result_path = os.path.join(os.path.dirname(__file__), 'result.json')
    with open(result_path, 'w') as f:
        json.dump(result, f)

    return jsonify(result)