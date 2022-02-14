import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time


time_stamp = time.strftime("%Y%m%d-%H%M%S")
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--headless")
chrome_options.add_argument("window-size=1400,800");
s = Service(executable_path='./chromedriver')
driver = webdriver.Chrome(service=s, options=chrome_options)
driver.get('https://www.krc.com.tr/contact-form')
contact_type = Select(driver.find_element(By.ID, 'ChannelId'))
contact_type.select_by_visible_text('E-Ticaret İletişim')

print("Contact type is selected")
complain_type = Select(driver.find_element(By.ID, 'RequestType'))
complain_type.select_by_visible_text('Şikayet')
print("Contact reason is selected")

driver.implicitly_wait(15)

try:
    close_overlay = driver.find_element(By.ID, 'vl-form-close')
    close_overlay.click()
except:
    print("No popup window")

SCROLL_PAUSE_TIME = 0.5

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

fields = {
    'custname': 'Ahmet',
    'CustSurName': 'Turkmen',
    'Email': os.getenv("EMAIL"),
    'phone': os.getenv("PHONE_NUMBER"),
    'Description':  os.getenv("COMPLAIN_MESSAGE")
}

for k, v in fields.items():
    driver.find_element(By.ID, k).send_keys(v)

time.sleep(7)
try:
    submit = driver.find_element(By.ID, 'customerContactFormSubmitWithRecaptcha')
    submit.click()
    message = driver.find_element(By.CLASS_NAME,"krc-alert info mb-2").text
    if message == "Form Başarıyla Gönderildi":
        driver.find_element(By.ID, 'Description').clear()  # do not leak message
        driver.save_screenshot('contact-page-{}.png'.format(time_stamp))
        print(message)
    else:
        print("Failed to submit form")
except:
    driver.find_element(By.ID, 'Description').clear()  # do not leak message
    driver.save_screenshot('contact-page-{}.png'.format(time_stamp))
