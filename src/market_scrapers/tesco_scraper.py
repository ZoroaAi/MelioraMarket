from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get("https://www.tesco.com/groceries/en-GB/shop/fresh-food/all")

product_names = driver.find_elements(By.XPATH, "//a[@class='styled__Anchor-sc-1xbujuz-0 csVOnh beans-link__anchor']//span[@class='styled__Text-sc-1xbujuz-1 ldbwMG beans-link__text']")
product_prices = driver.find_elements(By.XPATH,"//div[@class='base-components__RootElement-sc-1mosoyj-1 styled__Container-sc-8qlq5b-0 jptQqM bgZrjw styled__StyledPrice-sc-6nhkzi-5 iYHeik beans-buybox__price beans-price__container']//p[@class='styled__StyledHeading-sc-119w3hf-2 jWPEtj styled__Text-sc-8qlq5b-1 lnaeiZ beans-price__text']")
product_images = driver.find_elements(By.XPATH,"//div[@class='product-lists']//img[@class='styled__Image-sjvkdn-0 bJErKA product-image beans-responsive-image__image']")

i=0
for img in product_images:
    i=i+1
    # print(img.get_attribute('src'))
    print(f"{i}: {img.get_attribute('src')}")

# i = 0
# while i < len(product_names):
#     print("Names :"+product_names[i].text+"\nPrice: " + product_prices[i].text+ "\nImageSrc: "+ product_image[i].text) 
#     i = i + 1

driver.quit()