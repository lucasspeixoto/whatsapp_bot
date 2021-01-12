#-*- coding: utf_8 -*-
#encoding: utf-8



import tkinter as tk
import tkinter.messagebox
import time

from selenium.webdriver.remote.command import Command

def send_message(self):
    #print(self.obs.get(1.0, "end-1c"))
    '''
    #Verificação Se houve conexão
    try:
        self.driver.execute(Command.STATUS)
        pass
    except Exception as e:
        tkinter.messagebox.showerror("ERRO", "Navegador Fechado, realizar login.")
        return
    '''
    #Verificação se mensagem foi inserida
    if self.obs.get(1.0, "end-1c") == '':
        tkinter.messagebox.showerror("ERRO","Inserir Mensagem")
        return
    else:
        pass
    
    #Buscar listagem de contatos selecionados
    contact_list = [self.listbox.get(contact) for contact in self.listbox.curselection()]
    if len(contact_list) < 1:
        tkinter.messagebox.showerror("ERRO","Selecione ao menos um contato")
        return
    
    #Inicar loop nos contatos
    self.progress_bar.start(2)
    self.progress_bar.step(2)

    for contact in contact_list:
        print(contact)
    
    
    self.progress_bar.stop()
    tkinter.messagebox.showinfo("Finalizado" ,"Envio Finalizado")
    return