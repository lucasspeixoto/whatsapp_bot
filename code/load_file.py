#-*- coding: utf_8 -*-
#encoding: utf-8

import tkinter.messagebox
from tkinter import filedialog
import time

def load_img_or_video(self):
    #Selecionar Imagem/Video
    try:
        self.img_path = list(filedialog.askopenfilenames(
                            initialdir = "/", 
                            title = "Selecionar imagem"))[0]
        return
    except IndexError:
        time.sleep(0.3)
        tkinter.messagebox.showinfo("Status", "Nenhuma imagem selecionada.")
        return


def load_doc(self):
    #Selecionar arquivo
    try:
        self.file_path = list(filedialog.askopenfilenames(
                            initialdir = "/", 
                            title = "Selecionar Arquivo"))[0]                     
        return
    except IndexError:
        time.sleep(0.3)
        tkinter.messagebox.showinfo("Status", "Nenhum arquivo selecionado.")
        return