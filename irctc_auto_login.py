import json
from time import sleep
import pytesseract
from PIL import Image
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.implicitly_wait(10)

with open('config.json') as config_file:
    config_data = json.load(config_file)

username = config_data['username']
password = config_data['password']
boarding_station = config_data['from']
destination_station = config_data['to']
date_of_journey = config_data['date']


driver.get('https://www.irctc.co.in/nget/train-search')

dropdown_element = driver.find_element(By.CSS_SELECTOR, 'body > app-root > app-home > div.header-fix > app-header > div.h_container_sm > div.h_menu_drop_button.hidden-xs > a > i')
dropdown_element.click()
login_element = driver.find_element(By.CSS_SELECTOR, '#slide-menu > p-sidebar > div > nav > div > label > button')
login_element.click()

username_element = driver.find_element(By.XPATH, '/html/body/app-root/app-home/div[3]/app-login/p-dialog[1]/div/div/div[2]/div[2]/div/div[2]/div[2]/div[2]/form/div[1]/input')
username_element.send_keys(username)
password_element = driver.find_element(By.XPATH, '/html/body/app-root/app-home/div[3]/app-login/p-dialog[1]/div/div/div[2]/div[2]/div/div[2]/div[2]/div[2]/form/div[2]/input')
password_element.send_keys(password)

image_element = driver.find_element(By.XPATH, '/html/body/app-root/app-home/div[3]/app-login/p-dialog[1]/div/div/div[2]/div[2]/div/div[2]/div[2]/div[2]/form/div[4]/div/app-captcha/div/div/div[2]/span[1]/img')
image_data = image_element.screenshot_as_png

with open('image.png', 'wb') as f:
    f.write(image_data)

image = Image.open('image.png')
extracted_text = pytesseract.image_to_string(image).replace(" ","")
print(extracted_text)
captcha_text_element = driver.find_element(By.XPATH, '/html/body/app-root/app-home/div[3]/app-login/p-dialog[1]/div/div/div[2]/div[2]/div/div[2]/div[2]/div[2]/form/div[4]/div/app-captcha/div/div/input')
captcha_text_element.send_keys(extracted_text)

print("Login Successful: "+ "-"*10)
print("Adding journey details: " + "-"*10)

from_element = driver.find_element(By.XPATH, '/html/body/app-root/app-home/div[3]/div/app-main-page/div/div/div[1]/div[2]/div[1]/app-jp-input/div/form/div[2]/div[1]/div[1]/p-autocomplete/span/input')
from_element.send_keys(boarding_station)
sleep(0.5)
from_element.send_keys(Keys.TAB)
to_element = driver.find_element(By.XPATH, '/html/body/app-root/app-home/div[3]/div/app-main-page/div/div/div[1]/div[2]/div[1]/app-jp-input/div/form/div[2]/div[1]/div[2]/p-autocomplete/span/input')
to_element.send_keys(destination_station)
sleep(0.5)
to_element.send_keys(Keys.TAB)

date_element = driver.find_element(By.XPATH, '/html/body/app-root/app-home/div[3]/div/app-main-page/div/div/div[1]/div[2]/div[1]/app-jp-input/div/form/div[2]/div[2]/div[1]/p-calendar/span/input')
date_element.send_keys(Keys.CONTROL + "A")
date_element.send_keys(date_of_journey)

general_element = driver.find_element(By.XPATH, '/html/body/app-root/app-home/div[3]/div/app-main-page/div/div/div[1]/div[2]/div[1]/app-jp-input/div/form/div[3]/div/div/p-dropdown/div/div[2]/span')
general_element.click()
tatkal_element = driver.find_element(By.XPATH, '/html/body/app-root/app-home/div[3]/div/app-main-page/div/div/div[1]/div[2]/div[1]/app-jp-input/div/form/div[3]/div/div/p-dropdown/div/div[4]/div/ul/p-dropdownitem[6]/li')
tatkal_element.click()

search_button_element = driver.find_element(By.XPATH, '//*[@id="divMain"]/div/app-main-page/div/div/div[1]/div[2]/div[1]/app-jp-input/div/form/div[5]/div[1]/button')
search_button_element.click()

print("Will update for train selection and booking: " + "-"*10)

sleep(30)
driver.close()
