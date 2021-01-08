#-*- coding: utf_8 -*-
#encoding: utf-8

import tkinter as tk
import tkinter.messagebox
from tkinter import filedialog
import pandas as pd
import time

def load_contacts(self):

    try:
        contact_list_path = list(filedialog.askopenfilenames(initialdir = "/", 
                                                            title = "Selecionar arquivo com lista de contatos."))[0]
    except IndexError:
        time.sleep(0.3)
        tkinter.messagebox.showinfo("Status", "Nenhum arquivo selecionado")
        return

    #Extensão
    ext = contact_list_path.split("/")[-1].split(".")[-1]

    #filename = contact_list_path.split("/")[-1].split(".")[0]
    #file_path = "/".join(contact_list_path.split("/")[0:-1]) + "/"

    #Verificação do formato do Arquivo e leitura dos dados com transformação em uma lista.
    contacts = ''
    if ext in ['xlsx', 'xls']:
        contacts = pd.read_excel(contact_list_path)
        columm_name = contacts.columns[0]
        contacts = contacts[columm_name].tolist()
    elif ext == 'txt':
        with open(contact_list_path, encoding='utf-8') as f:
            contacts = [line.strip() for line in f]
            f.close()
    else:
        tkinter.messagebox.showerror("ERRO", "Formato inválido, converter em .xlsx, .xls ou .txt.")
        return

    #Popular Listbox
    self.listbox.insert(tk.END, *contacts)