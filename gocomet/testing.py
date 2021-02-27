from selenium import webdriver
import time
from bs4 import BeautifulSoup
import requests


#start



bot=webdriver.Chrome()
time.sleep(1)
bot.get('https://www.flipkart.com/search?q=mobiles')

for i in bot.find_elements_by_class_name('_2kHMtA'):
    print(i.find_element_by_class_name('_1fQZEK').get_attribute('href'))
    print(i.find_element_by_class_name('_4rR01T').text)
    print(i.find_element_by_class_name('_3LWZlK').text)
    print(i.find_element_by_xpath("//div[@class='_30jeq3 _1_WHN1']").text)

