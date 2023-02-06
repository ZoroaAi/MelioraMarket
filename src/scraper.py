from bs4 import BeautifulSoup
import requests
from selenium import webdriver

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)


driver.get("https://www.tesco.com/groceries/en-GB/shop/fresh-food/all")

# Getting element classes of names, prices, and images
names = driver.find_elements('xpath','//h3[@class="styles__H3-oa5soe-0 bCKNNq"]')
prices = driver.find_elements('xpath','//div[@class="styled__StyledHeading-sc-119w3hf-2 jWPEtj styled__Text-sc-8qlq5b-1 lnaeiZ beans-price__text"]')
images = driver.find_elements('xpath','//img[@class="styled__Image-sjvkdn-0 bJErKA product-image beans-responsive-image__image"]')

#  Extracting the text and URLs of images from elements
product_names = [name.text for name in names]
product_prices = [price.text for price in prices]
product_images = [image.get_attribute('src') for image in images]

# Store the extracted information
products = []
for name, price, image in zip(product_names, product_prices, product_images):
    product = {
        'name': name,
        'price': price,
        'image': image
    }
    products.append(product)

for i in range(0,5,1):
    print(products[i])


driver.close()