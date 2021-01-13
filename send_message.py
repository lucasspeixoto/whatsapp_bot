#-*- coding: utf_8 -*-
#encoding: utf-8

import tkinter as tk
import tkinter.messagebox
import time

from selenium.webdriver.remote.command import Command
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys  

def send_message(self):
    
    #Verificação Se houve conexão
    try:
        self.driver.execute(Command.STATUS)
        pass
    except Exception:
        tkinter.messagebox.showerror("ERRO", "Navegador Fechado, realizar login.")
        return
    
    #Buscar listagem de contatos selecionados
    contact_list = [self.listbox.get(contact) for contact in self.listbox.curselection()]
    if len(contact_list) < 1:
        tkinter.messagebox.showerror("ERRO","Selecione ao menos um contato")
        return

    ''' 
    Verificação se ao menos Mensagem de texto ou
    Mensagem de Imagem + Imagem ou 
    Arquivo foram selecionados
    '''
    text_msg = self.text_msg.get(1.0, "end-1c")
    text_img = self.text_img.get(1.0, "end-1c")
    if (text_msg == '') and (text_img == '') and (hasattr(self, 'file_path') == False):
        tkinter.messagebox.showerror("ERRO","""Inserir Mensagem de Texto, \
Mensagem de Imagem com anexo ou Arquivo.""")
        return
    else:
        pass
    
    #Verificar se imagem foi selecionada caso exista texto no campo 'Mensagem de Imagem'
    if (text_img != '') and (hasattr(self, 'img_path') == False):
        tkinter.messagebox.showerror("ERRO","""Selecionar Imagem para ser anexada junto \
ao texto digitado.""")
        return
    else:
        pass

    #Inicar loop nos contatos
    self.progress_bar.start(2)
    self.progress_bar.step(2)

    for contact in contact_list:
        #Selecionar Campo de pesquisa de contato
        search_xpath ='//*[@id="side"]/div[1]/div/label/div/div[2]'
        elem = self.driver.find_element_by_xpath(search_xpath)
        elem.click()
        time.sleep(2)

        #Digitar contato e Clicar 'ENTER'
        elem.send_keys(contact)
        time.sleep(0.5)
        ActionChains(self.driver).send_keys(Keys.ENTER).perform()
        time.sleep(1)
        
        #Inserir Mensagem
        if text_msg != '':
            input_xpath = '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]'
            found = self.driver.find_element_by_xpath(input_xpath)
            time.sleep(0.5)
            found.send_keys(text_msg + Keys.ENTER)
        else:
            pass

        #Inserir imagem/video
        if text_img != '':
            #Inserir Imagem/Video
            clipButton = self.driver.find_element_by_xpath('''//*[@id="main"]/footer/
            div[1]/div[1]/div[2]/div/div/span''')
            clipButton.click()
            time.sleep(1)

            mediaButton = self.driver.find_element_by_xpath('''//*[@id="main"]/footer/div[1]/div[1]/
            div[2]/div/span/div/div/ul/li[1]/button/input''')
            mediaButton.send_keys(self.img_path)
            time.sleep(1)

            messageField = self.driver.find_element_by_xpath('''//*[@id="app"]/div/div/div[2]/
            div[2]/span/div/span/div/div/div[2]/div[1]/span/div/div[2]/
            div/div[3]/div[1]/div[2]''')
            messageField.send_keys(text_img)
            time.sleep(1)

            sendButton = self.driver.find_element_by_xpath('''//*[@id="app"]/div/div/div[2]/div[2]/span/
            div/span/div/div/div[2]/span/div/div/span''')
            sendButton.click()

        else:
            pass

        #Inserir Arquivo
        if hasattr(self, 'file_path') == True:
            clipButton = self.driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[1]/div[2]/div/div/span')
            clipButton.click()
            time.sleep(1)

            mediaButton = self.driver.find_element_by_xpath('''//*[@id="main"]/footer/div[1]/div[1]/
            div[2]/div/span/div/div/ul/li[3]/button/input''')
            mediaButton.send_keys(self.file_path)
            time.sleep(1)

            sendButton = self.driver.find_element_by_xpath('''//*[@id="app"]/div/div/div[2]/div[2]/span/
            div/span/div/div/div[2]/span/div/div/span''')
            sendButton.click()
        else:
            pass

    self.progress_bar.stop()
    tkinter.messagebox.showinfo("Finalizado" ,"Envio Finalizado")
    return