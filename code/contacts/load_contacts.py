# -*- coding: utf_8 -*-
#encoding: utf-8

import tkinter.messagebox
from tkinter import filedialog
import pandas as pd
import time

from contacts.make_listbox import create_box


def load_contacts(self):

    # Limpar Contatos anteriores
    self.listbox.delete('0', 'end')

    # Verificação Se ao menos um item foi selecionado.
    try:
        contact_list_path = list(filedialog.askopenfilenames(
            initialdir="/",
            title="Selecionar arquivo com a lista de contatos."))[0]
    except IndexError:
        time.sleep(0.3)
        tkinter.messagebox.showinfo("Status", "Nenhum arquivo selecionado.")
        return

    # Leitura do arquivo
    self.base = pd.read_excel(contact_list_path)

    # Montagem da lista no listbox
    self.contacts = create_box(self.base)
    for i in range(0, len(self.contacts)):
        self.listbox.insert(i, self.contacts[i])

    tkinter.messagebox.showinfo("Status", "Lista carregada")
    return
