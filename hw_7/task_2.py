import time

from selenium import webdriver
from pymongo import MongoClient
from selenium.webdriver.common.by import By
from selenium.common import exceptions

client = MongoClient('localhost', 27017)
mongo_base = client.mvideo
collection = mongo_base['goods_of_the_day']

driver = webdriver.Chrome()
url = 'https://www.mvideo.ru/'
driver.get(url)
driver.implicitly_wait(10)

while True:
    try:
        next_button = driver.find_element(By.XPATH,
                 '//mvid-day-products-block[@class="block ng-star-inserted"]//button[@class="btn forward mv-icon-button--primary mv-icon-button--shadow mv-icon-button--medium mv-button mv-icon-button"]')
        driver.implicitly_wait(3)
        next_button.click()
        driver.implicitly_wait(3)
    except exceptions.StaleElementReferenceException:
        break
    except exceptions.ElementNotInteractableException:
        break

goods_of_the_day_list = driver.find_elements(By.XPATH,
                                             '//mvid-day-products-block[@class="block ng-star-inserted"]//div[@class="product ng-star-inserted"]')
for good in goods_of_the_day_list:
    item = {}
    item['name'] = good.find_element(By.XPATH, './/div[@class="title"]//a').text
    item['link'] = good.find_element(By.XPATH, './/div[@class="title"]//a').get_attribute('href')
    item['price'] = good.find_element(By.XPATH, './/span[@class="price__main-value"]').text
    collection.insert_one(item)
driver.quit()
