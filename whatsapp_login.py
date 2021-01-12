#-*- coding: utf_8 -*-
#encoding: utf-8

from selenium import webdriver 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support import expected_conditions as EC

import tkinter.messagebox
import time

def whatsapp_login(self):

    link = "https://web.whatsapp.com/"

    #Verificação da Conexão
    self.driver = webdriver.Chrome(executable_path=self.path_chromedriver) 
    try:
        self.driver.get(link)
    except WebDriverException:
        self.driver.quit()
        tkinter.messagebox.showerror("ERRO", "Verificar Internet.")
        return

    #Aguardar Até QR Code ser Scaneado
    search_xpath = '//*[@id="side"]/div[1]/div/label/div/div[2]'
    try:
        elem = WebDriverWait(self.driver, 200).until(
        EC.presence_of_element_located((By.XPATH, search_xpath))
        )
    finally:  
        try:
            elem.click()
            self.driver.maximize_window() 
        except UnboundLocalError:
            self.driver.quit()
            tkinter.messagebox.showerror("ERRO", "Tempo Expirado, logar novamente.")
            return
    
    time.sleep(0.5)
    tkinter.messagebox.showinfo("Status", "QR Code Scanned")
    return