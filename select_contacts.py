#-*- coding: utf_8 -*-
#encoding: utf-8

import tkinter.messagebox

def select_contacts(self):
    #Verificar se Contatos foram carregados


    self.selected_contacts = [self.listbox.get(contact) 
                                for contact in self.listbox.curselection()]

    if len (self.selected_contacts) == 0:
        tkinter.messagebox.showerror("ERRO", "Carregar Contatos.")
        return

    print(self.selected_contacts)

    return