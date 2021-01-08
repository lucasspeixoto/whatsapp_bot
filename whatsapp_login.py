#-*- coding: utf_8 -*-
#encoding: utf-8

from selenium import webdriver 
from selenium.webdriver.support.ui import WebDriverWait 


def whatsapp_login(self):

    link = "https://web.whatsapp.com/"

    driver = webdriver.Chrome(self.path_chromedriver) 
    driver.get(link)
    inp_xpath_search = '//*[@id="side"]/div[1]/div/label/div/div[2]'
    input_box_search = WebDriverWait(driver,20).until(lambda driver: driver.find_element_by_xpath(inp_xpath_search))
    input_box_search.click()
    
    driver.maximize_window()


    return