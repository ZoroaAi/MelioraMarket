from itertools import zip_longest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

tesco_prod_list = {}


driver.get("https://www.tesco.com/groceries/en-GB/shop/fresh-food/all")

product_container = driver.find_elements(By.XPATH,"//div[@class='product-list--list-item']")

for product in product_container:
    # Wait for all product images to be present on the page
    wait = WebDriverWait(driver, 10)

    # Find Elements containing the information
    product_names = driver.find_elements(By.XPATH, "div[@class='product-lists']//a[@class='styled__Anchor-sc-1xbujuz-0 csVOnh beans-link__anchor']//span[@class='styled__Text-sc-1xbujuz-1 ldbwMG beans-link__text']")
    product_prices = driver.find_elements(By.XPATH,"div[@class='product-lists']//div[@class='base-components__RootElement-sc-1mosoyj-1 styled__Container-sc-8qlq5b-0 jptQqM bgZrjw styled__StyledPrice-sc-6nhkzi-5 iYHeik beans-buybox__price beans-price__container']//p[@class='styled__StyledHeading-sc-119w3hf-2 jWPEtj styled__Text-sc-8qlq5b-1 lnaeiZ beans-price__text']")
    product_images = wait.until(EC.presence_of_all_elements_located((By.XPATH,"//div[@class='product-lists']//img[@class='styled__Image-sjvkdn-0 bJErKA product-image beans-responsive-image__image']")))

    # Append data to dictionary
    for name, price, item in zip_longest(product_names, product_prices, product_images, fillvalue=None):
        if name is None or price is None or item is None:
            continue
        
        name = name.text
        price = price.text
        src_firstLink = item.get_attribute('srcset').split(',')[0]
        img_src = src_firstLink.replace(' 768w','')
        
        tesco_prod_dict = {}
        tesco_prod_dict['title'] = name
        tesco_prod_dict['price'] = price
        tesco_prod_dict['image'] = img_src
        
        tesco_prod_list.append(tesco_prod_dict)
        
    # Next Page Button
    # butt = driver.find_element(By.XPATH, "//a[@class='pagination--button prev-next']")
    # butt.click()
    

print(tesco_prod_list)

# wait.until(EC.presence_of_all_elements_located((By.XPATH,"//div[@class='product-lists']//img[@class='styled__Image-sjvkdn-0 bJErKA product-image beans-responsive-image__image']")))

# for i, img in product_images:
#     counter = counter + 1
#     src_firstLink = img.get_attribute('srcset').split(',')[0]
#     print(f"{i}: {src_firstLink.replace(' 768w','')}")

driver.quit()