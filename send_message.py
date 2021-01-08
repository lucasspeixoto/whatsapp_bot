#-*- coding: utf_8 -*-
#encoding: utf-8



import tkinter as tk
import tkinter.messagebox
import time

from selenium.webdriver.remote.command import Command

def send_message(self):

    #Verificação Se houve conexão
    try:
        self.driver.execute(Command.STATUS)
        pass
    except Exception as e:
        tkinter.messagebox.showerror("ERRO", "Navegador Fechado, realizar login.")
        return