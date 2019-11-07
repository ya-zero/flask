from selenium import webdriver
from selenium.webdriver.common.by import By
import time
driver = webdriver.Chrome('/usr/lib/chromium/chromedriver')
driver.get('http://reinfokom.ru')
time.sleep(2)
driver.save_screenshot('reinfo.png')
driver.find_element_by_link_text('Контакты').click()
time.sleep(2)
driver.save_screenshot('reinfo_contact.png')
driver.quit()