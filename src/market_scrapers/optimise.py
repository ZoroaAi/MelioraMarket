from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

data = []
pageNumber = 2
base_url = "https://www.tesco.com/groceries/en-GB/shop/fresh-food/all?page="

timeout = 5
wait = WebDriverWait(driver, timeout)

# Scrape next pages:
for page in range(1, pageNumber + 1):
    url = base_url + str(page)
    driver.get(url)
    product_container = driver.find_elements(By.XPATH, "//li[contains(@class, 'product-list--list-item')]")
    
    products = []
    for product in product_container:
        title = product.find_element(By.XPATH, ".//a[@class='styled__Anchor-sc-1xbujuz-0 csVOnh beans-link__anchor']//span[@class='styled__Text-sc-1xbujuz-1 ldbwMG beans-link__text']").text
        img = product.find_element(By.XPATH, ".//div[@class='product-image__container']//img")\
                     .get_attribute('srcset').split(',')[0].replace(' 768w','')
        try:
            price = wait.until(EC.presence_of_element_located((By.XPATH, ".//p[@class='styled__StyledHeading-sc-119w3hf-2 jWPEtj styled__Text-sc-8qlq5b-1 lnaeiZ beans-price__text']"))).text
        except NoSuchElementException:
            price = 'Out of Stock'
            print("Out of Stock")
            
        products.append({
            'title': title,
            'img': img,
            'price': price
        })
    
    data.extend(products)

    for j, product in enumerate(products):
        # Print data collected:
        print(f"{j}: {product['title']}")
        print(f"{product['price']}")
        print(f"{product['img']}")
        
json_data = json.dumps(data)
with open("src/scraped_data/tesco_data1.json", 'w') as file:
    file.write(json_data)