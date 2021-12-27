from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient
from selenium.common import exceptions


def parse_email(element):
    item = {}
    item['from'] = WebDriverWait(element, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '//span[@class="Sender__email--20L3t qa-MessageViewer-SenderEmail"]'))).text
    item['date'] = WebDriverWait(element, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '//a[@class="Header__dateLink--3dYKV qa-MessageViewer-Header-dateLink"]'))).text
    item['subject'] = WebDriverWait(element, 10).until(
        EC.presence_of_element_located(
            (By.CLASS_NAME, 'Title__subject--34siJ'))).text
    item['subject'] = WebDriverWait(element, 10).until(
        EC.presence_of_element_located(
            (By.CLASS_NAME, 'MessageBody__body--1pLiq'))).text
    return item


if __name__ == '__main__':
    user_login = ''  # ввести логин почты
    user_passwd = ''  # ввести пароль от почты

    client = MongoClient('localhost', 27017)
    mongo_base = client.mail
    collection = mongo_base['messages']

    driver = webdriver.Chrome()
    url = 'https://yandex.ru/'
    driver.get(url)

    mail_button = driver.find_element(By.CSS_SELECTOR,
                                      'a[class="home-link desk-notif-card__login-new-item desk-notif-card__login-new-item_mail home-link_black_yes"]')
    mail_button.click()
    driver.switch_to.window(driver.window_handles[1])

    field_login = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'passp-field-login')))
    print(driver.title)
    field_login.send_keys(user_login)
    field_login.send_keys(Keys.ENTER)
    field_passwd = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'passp-field-passwd')))
    field_passwd.send_keys(user_passwd)
    field_passwd.send_keys(Keys.ENTER)

    first_message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CLASS_NAME, 'ns-view-messages-item-wrap')
        )
    )
    first_message.click()

    while True:
        try:
            collection.insert_one(parse_email(driver))
            next_mail = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, 'след.')))
            next_mail.click()
        except exceptions.TimeoutException:
            print('The end')
            break
    driver.quit()
