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
for page in range(1,pageNumber+1):
    url = base_url + str(page)
    driver.get(url)
    product_container = driver.find_elements(By.XPATH,"//li[@class='product-list--list-item']")
    
    for j, product in enumerate(product_container, start=0):
        # Find Elements containing the information
        product_names = product.find_element(By.XPATH, ".//a[@class='styled__Anchor-sc-1xbujuz-0 csVOnh beans-link__anchor']//span[@class='styled__Text-sc-1xbujuz-1 ldbwMG beans-link__text']")
        product_images = product.find_element(By.XPATH,".//div[@class='product-image__container']//img")
        try:
            product_prices = wait.until(EC.presence_of_element_located((By.XPATH,".//p[@class='styled__StyledHeading-sc-119w3hf-2 jWPEtj styled__Text-sc-8qlq5b-1 lnaeiZ beans-price__text']")))
        except NoSuchElementException:
            price = "Out of Stock"
            print("Out of Stock")
            continue
        
        name =product_names.text
        price = product_prices.text
        src_firstLink = product_images.get_attribute('srcset').split(',')[0]
        img_src = src_firstLink.replace(' 768w','')
        
        # Print data collected:
        print(f"{j}: {name}")
        print(f"{price}")
        print(f"{img_src}")
        
        data.append({'title': name,'price': price,'img': img_src})
    
    

json_data = json.dumps(data)
# file_path = os.path.join("\scraped_data", "data.json")
with open("src/scraped_data/tesco_data.json", 'w') as file:
    file.write(json_data)

driver.quit()