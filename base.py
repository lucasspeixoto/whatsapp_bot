#-*- coding: utf_8 -*-
#encoding: utf-8

from ttkthemes import themed_tk
import tkinter as tk
from tkinter import ttk
import tkinter.font as font
import tkinter.messagebox
import threading
import sys

import os
import inspect

from PIL import Image, ImageTk

from whatsapp_login import whatsapp_login
from load_contacts import load_contacts
from select_contacts import select_contacts
from load_file import load_img_or_video, load_doc
from send_message import send_message

class Geral(themed_tk.ThemedTk):
    def __init__(self, *args, **kwargs):
        themed_tk.ThemedTk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        menu = tk.Menu(container)
        
        windows = tk.Menu(menu, tearoff=0, bg='white',activebackground='#4fc65a')
        options = tk.Menu(menu, tearoff=0, bg='white',activebackground='#4fc65a')

        menu.add_cascade(menu=windows,underline=1,label="Janelas")
        menu.add_cascade(menu=options,underline=1,label="Opções")
        
        windows.add_command(label="Whatsapp",
            command=lambda:threading.Thread(target=self.show_frame(Whatsapp),daemon=True).start())
        windows.add_command(label="Ajuda",
            command=lambda:threading.Thread(target=self.show_frame(Ajuda),daemon=True).start())

        options.add_command(label="Sair",
            command=lambda:threading.Thread(target=self.quit,daemon=True).start())
        options.add_command(label="Observações",
            command=lambda:threading.Thread(target=self.show_help,daemon=True).start())

        themed_tk.ThemedTk.config(self, menu=menu)

        for Frame, geometry, state in zip((Whatsapp, Ajuda), ('850x600+0+0', '850x600+0+0'), ('normal', 'normal')):
            frame = Frame(parent=container, controller=self)
            self.frames[Frame] = (frame, geometry, state)
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Whatsapp)

    def show_frame(self, cont):
        frame, geometry, state = self.frames[cont]
        self.update_idletasks()
        self.geometry(geometry)
        self.state(state)
        frame.tkraise()

    def onexit(self):
        sys.exit(0)

    def show_help(self):
        text = '''Observações Importantes: \n
➣ .
'''
        tkinter.messagebox.showinfo("Ajuda",text)

class Ajuda(ttk.Frame):   
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.place(relheight=1, relwidth=1)
        
        font.nametofont("TkTextFont").configure(size=12)
        font.nametofont("TkDefaultFont").configure(size=12)

class Whatsapp(ttk.Frame):   
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.place(relheight=1, relwidth=1)
        
        font.nametofont("TkTextFont").configure(size=12)
        font.nametofont("TkDefaultFont").configure(size=12)
        
        #Definições Globais
        #Caminho Raiz
        self.path_folder = os.getcwd() + '/'

        #Variáveis Selenium
        self.path_chromedriver = self.path_folder + 'Driver/chromedriver.exe'

        #Diretório Download
        self.path_down = os.path.expanduser(os.getenv("USERPROFILE")).replace("\\","/") + "/Downloads/"

        #Título
        title_label = ttk.Label(self, text="Comunicação com Clientes - WhatsApp", font='segoe 24 bold')
        title_label.place(relx=0.005,rely=0.04,relwidth=0.72,relheight=0.07, anchor='w')

        #Título Login
        log_label = ttk.Label(self, text="Logar", font='segoe 18 bold')
        log_label.place(relx=0.005,rely=0.12,relwidth=0.08,relheight=0.05, anchor='w')

        #Botão de Login no WhatsApp Web
        log_bt = ttk.Button(self,
                    text="Whatsapp Web", 
                    command = lambda: threading.Thread(target = self.f1, daemon = True).start())
        log_bt.place(relx=0.10,rely=0.12,relwidth=0.14,relheight=0.05, anchor='w')

        #Título Listbox
        listbox_label = ttk.Label(self, text="Lista de Contatos", font='segoe 18 bold')
        listbox_label.place(relx=0.005,rely=0.20,relwidth=0.25,relheight=0.05, anchor='w')

        #Criação Listbox
        self.listbox = tk.Listbox(self, 
                        background='#dcffd4',
                        relief='solid',
                        foreground='#000000',
                        font='segoe 10 bold',
                        selectmode='extended'
                            )
        self.listbox.place(relx=0.005,rely=0.57,relwidth=0.40,relheight=0.68, anchor='w')
        self.scrollbar_list_y = ttk.Scrollbar(self, orient="vertical")
        self.scrollbar_list_y.config(command=self.listbox.yview)
        self.scrollbar_list_y.place(relx=0.40,rely=0.57, relwidth=0.015, relheight=0.68, anchor='w')
        self.listbox.config(yscrollcommand=self.scrollbar_list_y.set)
        self.scrollbar_list_x = ttk.Scrollbar(self, orient="horizontal")
        self.scrollbar_list_x.config(command=self.listbox.xview)
        self.scrollbar_list_x.place(relx=0.005,rely=0.91, relwidth=0.40, relheight=0.020, anchor='w')
        self.listbox.config(xscrollcommand=self.scrollbar_list_x.set)
        
        #Botão para carregar contatos
        load_bt = ttk.Button(self,
                    text="Carregar", 
                    command = lambda: threading.Thread(target = self.f2, daemon = True).start())
        load_bt.place(relx=0.005,rely=0.955,relwidth=0.10,relheight=0.05, anchor='w')

        #Botão para selecionar contatos
        select_bt = ttk.Button(self,
                    text="Selecionar", 
                    command = lambda: threading.Thread(target = self.f3, daemon = True).start())
        select_bt.place(relx=0.30,rely=0.955,relwidth=0.10,relheight=0.05, anchor='w')

        #Título mensagem
        msg_label = ttk.Label(self, text="Mensagem", font='segoe 18 bold')
        msg_label.place(relx=0.43,rely=0.12,relwidth=0.20,relheight=0.05, anchor='w')

        #Caixa de Mensagem
        self.obs = tk.Text(self, 
                        fg="#2b39b5", 
                        bg="white", 
                        font = "-family {Segoe UI} -size 16"
                            )
        self.obs.place(relx=0.43, rely=0.53, relwidth=0.55, relheight=0.75, anchor = 'w')
        self.scrollbar_obs_y = ttk.Scrollbar(self, orient="vertical")
        self.scrollbar_obs_y.config(command=self.obs.yview)
        self.scrollbar_obs_y.place(relx=0.97,rely=0.53, relwidth=0.015, relheight=0.75, anchor='w')
        self.obs.config(yscrollcommand=self.scrollbar_obs_y.set)

        #Título Anexos
        anexo_label = ttk.Label(self, text="Anexos", font='segoe 18 bold')
        anexo_label.place(relx=0.43,rely=0.955,relwidth=0.20,relheight=0.05, anchor='w')

        #Botão para carregar Imagem ou Video
        img_or_video_bt = ttk.Button(self,
                    text="Imagem", 
                    command = lambda: threading.Thread(target = self.f4, daemon = True).start())
        img_or_video_bt.place(relx=0.55,rely=0.955,relwidth=0.08,relheight=0.05, anchor='w')

        #Botão para carregar Arquivo
        file_bt = ttk.Button(self,
                    text="Arquivo", 
                    command = lambda: threading.Thread(target = self.f5, daemon = True).start())
        file_bt.place(relx=0.64,rely=0.955,relwidth=0.08,relheight=0.05, anchor='w')

        #Botão para Enviar mensagens
        send_bt = ttk.Button(self,
                    text="Enviar", 
                    command = lambda: threading.Thread(target = self.f6, daemon = True).start())
        send_bt.place(relx=0.73,rely=0.955,relwidth=0.08,relheight=0.05, anchor='w')

        #Barra de Progresso
        self.progress_bar = ttk.Progressbar(self, length= 80, mode = 'indeterminate')
        self.progress_bar.place(relx=0.82,rely=0.955,relwidth=0.15,relheight=0.05, anchor='w')

    def f1(self): whatsapp_login(self)

    def f2(self): load_contacts(self)

    def f3(self): select_contacts(self)

    def f4(self): load_img_or_video(self)

    def f5(self): load_doc(self)

    def f6(self): send_message(self)

def main():
    
    app = Geral()
    style = ttk.Style()  
    style.theme_use('scidgreen')
    style.configure('.', background='white')
    style.configure('my.TFrame', background='white', foreground ='black', font = "segoe 9 bold")
    style.configure('TRadiobutton', background="white", foreground='black', font = 'segoe 10 bold', justify='top', side='w')
    style.configure('TButton', background ='white', foreground ='black', font = 'segoe 10 bold')
    style.configure('down.TButton', background ='white', foreground ='green', font = 'segoe 18 bold', justify = 'c')
    style.configure('ok.TButton', background ='white', foreground ='green', font = 'segoe 16 bold', justify = 'c')
    style.configure('nok.TButton', background ='white', foreground ='red', font = 'segoe 16 bold', justify = 'c')
    style.configure('Icon.TButton', background ='white', foreground ='black', font = 'segoe 16 bold', justify = 'c')
    style.configure('TListbox',selectbackground='#7aad4b',relief='solid',foreground='#000000',selectmode='extended',font='segoe 10 bold',exportselection=0)
    style.configure('infP.TFrame', background='#f5eace', foreground ='black', font = "segoe 12 bold")
    style.configure("inf.TLabel", background ='#f5eace', foreground ='black', font = "segoe 8 bold")
    style.configure('TEntry', background ='white', foreground ="#0000B3", font = "segoe 12 bold")
    style.configure('input.TEntry', background ='white', foreground ="#0000B3", font = "segoe 10 bold")
    style.configure('infP.TEntry', background="#f5eace", foreground="#0000B3", font = "segoe 12 bold", justify='top', side='w')

    style.configure("head.Treeview",background = "#a0c882",foreground="black")
    style.configure("first.Treeview", background ='#a0c882', foreground ='black', font = "segoe 9 bold", relief = 'solid')
    style.configure("second.Treeview", background ='#b6c5f2', foreground ='black', font = "segoe 9 bold", relief = 'solid')
    style.configure("third.Treeview", background ='#8dddeb', foreground ='black', font = "segoe 9 bold", relief = 'solid')    
    style.configure("fourth.Treeview", background ='#eb8d8d', foreground ='black', font = "segoe 9 bold", relief = 'solid') 
    style.configure("fifth.Treeview", background ='#b36307', foreground ='black', font = "segoe 9 bold", relief = 'solid')
    style.configure("sixth.Treeview", background ='#e3ab66', foreground ='black', font = "segoe 9 bold", relief = 'solid')
    style.configure("seventh.Treeview", background ='#c94747', foreground ='black', font = "segoe 9 bold", relief = 'solid')
    style.configure("eighth.Treeview", background ='#b4e61d', foreground ='black', font = "segoe 9 bold", relief = 'solid')
    style.configure("ninth.Treeview", background ='#e3d288', foreground ='black', font = "segoe 9 bold", relief = 'solid')   

    app.title("Automatização Mensagens - WhatsApp")
    current_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0])) + "\\"
    app.iconbitmap(current_folder + "Imagens/logo.ico")
    
    #app.state("zoomed")
    app.mainloop()

if __name__=="__main__":
    main()
