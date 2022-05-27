# -*- coding: utf_8 -*-
# encoding: utf-8

import time
import tkinter.messagebox

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


def whatsapp_login(self):

    # url whatsapp web
    self.link = 'https://web.whatsapp.com/'

    self.options = webdriver.ChromeOptions()
    self.options.add_argument('--disable-infobars')
    self.options.add_argument('--start-maximized')
    self.options.add_argument('--disable-popup-blocking')
    self.options.add_argument('--disable-extensions')

    # Disable the banner "Chrome is being controlled by automated test software"
    self.options.add_experimental_option("useAutomationExtension", False)
    self.options.add_experimental_option(
        "excludeSwitches", ['enable-automation'])

    # Configurações do Navegador
    self.prefs = {
        "safebrowsing.enabled": False,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True,
        "profile.default_content_setting_values.automatic_downloads": 1
    }

    self.options.add_experimental_option('prefs', self.prefs)
    self.capabilities = DesiredCapabilities().CHROME
    self.capabilities.update(self.options.to_capabilities())

    # Verificação se Página não foi Fechada
    try:
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=self.options,
            desired_capabilities=self.capabilities)
    except WebDriverException:
        tkinter.messagebox.showerror(
            'ERRO', 'Página Fechada. Realizar Login novamente.')
        return

    # Verificação da Conexão
    try:
        self.driver.get(self.link)
        time.sleep(8)
    except WebDriverException:
        self.driver.quit()
        tkinter.messagebox.showerror('ERRO', 'Verificar Internet.')
        return

    # Aguardar Até QR Code ser Scaneado
    search_xpath = '''//*[@id='side']/div[1]/div/label/div/div[2]'''
    try:
        elem = WebDriverWait(self.driver, 200).until(
            EC.presence_of_element_located((By.XPATH, search_xpath))
        )
    finally:
        try:
            elem.click()
            time.sleep(2)
        except UnboundLocalError:
            self.driver.quit()
            tkinter.messagebox.showerror(
                'ERRO', 'Tempo Expirado, logar novamente.')
            return

    time.sleep(2)
    tkinter.messagebox.showinfo('Status', 'QR Code Scanned')
    time.sleep(2)
    return
