#-*- coding: utf_8 -*-
#encoding: utf-8

import tkinter as tk
import tkinter.messagebox
from tkinter import filedialog
import pandas as pd
import time

def load_contacts(self):

    #Limpar Contatos anteriores
    self.listbox.delete('0','end')
    
    #Verificação Se ao menos um item foi selecionado.
    try:
        contact_list_path = list(filedialog.askopenfilenames(
                            initialdir = "/", 
                            title = "Selecionar arquivo com a lista de contatos."))[0]
    except IndexError:
        time.sleep(0.3)
        tkinter.messagebox.showinfo("Status", "Nenhum arquivo selecionado.")
        return

    #Extensão
    ext = contact_list_path.split("/")[-1].split(".")[-1]

    #filename = contact_list_path.split("/")[-1].split(".")[0]
    #file_path = "/".join(contact_list_path.split("/")[0:-1]) + "/"

    #Verificação do formato do Arquivo e leitura dos dados com transformação em uma lista.
    self.contacts = ''
    if ext in ['xlsx', 'xls']:
        self.contacts = pd.read_excel(contact_list_path)
        columm_name = self.contacts.columns[0]
        self.contacts = self.contacts[columm_name].tolist()
    elif ext == 'txt':
        with open(contact_list_path, encoding='utf-8') as f:
            self.contacts = [line.strip() for line in f]
            f.close()
    else:
        tkinter.messagebox.showerror("ERRO",
         '''Formato inválido, converter em .xlsx, .xls ou .txt.''')
        return

    #Popular Listbox
    self.listbox.insert(tk.END, *self.contacts)

    return