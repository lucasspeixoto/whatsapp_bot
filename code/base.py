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

from PIL import ImageTk,Image

from whatsapp_login import whatsapp_login
from load_contacts import load_contacts
from load_file import load_img_or_video, load_doc
from send_message import send_message
from clear_path import clear_img_path, clear_file_path


class Geral(themed_tk.ThemedTk):
    def __init__(self, *args, **kwargs):
        themed_tk.ThemedTk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        menu = tk.Menu(container)
        
        windows = tk.Menu(menu, tearoff=0, bg='white',activebackground='#163537')
        options = tk.Menu(menu, tearoff=0, bg='white',activebackground='#163537')

        menu.add_cascade(menu=windows,underline=1,label="Janelas")
        menu.add_cascade(menu=options,underline=1,label="Opções")
        
        windows.add_command(label="Whatsapp",
            command=lambda:threading.Thread(target=self.show_frame(Whatsapp),daemon=True).start())
        windows.add_command(label="Help",
            command=lambda:threading.Thread(target=self.show_frame(Help),daemon=True).start())

        options.add_command(label="Sair",
            command=lambda:threading.Thread(target=self.quit,daemon=True).start())
        options.add_command(label="Observações",
            command=lambda:threading.Thread(target=self.show_help,daemon=True).start())

        themed_tk.ThemedTk.config(self, menu=menu)

        for Frame, geometry, state in zip((Whatsapp, Help), ('850x600+0+0', '850x600+0+0'), ('normal', 'normal')):
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

class BkgrFrameWhats(tk.Frame):
    def __init__(self, parent, file_path, width, height):
        super(BkgrFrameWhats, self).__init__(parent, borderwidth=0, highlightthickness=0)

        self.canvas = tk.Canvas(self, width=width, height=height)
        self.canvas.pack()

        pil_img = Image.open(file_path)
        self.img = ImageTk.PhotoImage(pil_img.resize((width, height), Image.ANTIALIAS))
        self.bg = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img)

        #Título
        self.canvas.create_text(5, 25, 
                        text="Automatização Envio de Mensagem - WhatsApp", 
                        fill="white", 
                        anchor='w', 
                        font=("arial bold", 28)
                        )

        #Login
        self.canvas.create_text(5, 70, 
                        text="Login", 
                        fill="white", 
                        anchor='w', 
                        font=("arial bold", 20)
                        )

        #Lista de Contatos
        self.canvas.create_text(5, 115, 
                        text="Lista de Contatos", 
                        fill="white", 
                        anchor='w', 
                        font=("arial bold", 20)
                        )

        #Caixa de Texto 1
        self.canvas.create_text(365, 65, 
                        text="Mensagem de Texto", 
                        fill="white", 
                        anchor='w', 
                        font=("arial bold", 20)
                        )

        #Caixa de Texto 2
        self.canvas.create_text(365, 285, 
                        text="Mensagem de Imagem", 
                        fill="white", 
                        anchor='w', 
                        font=("arial bold", 20)
                        )
        #Anexo
        self.canvas.create_text(365, 510, 
                        text="Anexos", 
                        fill="white", 
                        anchor='w', 
                        font=("arial bold", 20)
                        )

    def add(self, widget, x, y):
        canvas_window = self.canvas.create_window(x, y, anchor=tk.NW, window=widget)
        return widget

class BkgrFrameHelp(tk.Frame):
    def __init__(self, parent, file_path, width, height):
        super(BkgrFrameHelp, self).__init__(parent, borderwidth=0, highlightthickness=0)

        self.canvas = tk.Canvas(self, width=width, height=height)
        self.canvas.pack()

        pil_img = Image.open(file_path)
        self.img = ImageTk.PhotoImage(pil_img.resize((width, height), Image.ANTIALIAS))
        self.bg = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img)

    def add(self, widget, x, y):
        canvas_window = self.canvas.create_window(x, y, anchor=tk.NW, window=widget)
        return widget

class Help(ttk.Frame):   
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.place(relheight=1, relwidth=1)

        #Definições Globais

        #Caminho Executável
        self.current_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0])) + "\\"

        #Caminho Raiz
        self.root = "/".join(self.current_folder.split("\\")[0:-2]) + "/"
        
        #Fontes
        font.nametofont("TkTextFont").configure(size=12)
        font.nametofont("TkDefaultFont").configure(size=12)

        #Plano de Fundo
        IMAGE_PATH = self.root + "images/back.jpg"
        WIDTH, HEIGTH = 850, 600
        bkrgframe = BkgrFrameHelp(self, IMAGE_PATH, WIDTH, HEIGTH)
        bkrgframe.pack()


class Whatsapp(ttk.Frame):   
    def __init__(self, parent, controller):
        super().__init__(parent)

        
        self.place(relheight=1, relwidth=1)
        
        #Fontes
        font.nametofont("TkTextFont").configure(size=12)
        font.nametofont("TkDefaultFont").configure(size=12)

        #Variáveis
        self.per = tk.StringVar()
        
        #Definições Globais

        #Caminho Executável
        self.current_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0])) + "\\"

        #Caminho Raiz
        self.root = "/".join(self.current_folder.split("\\")[0:-2]) + "/"

        #Plano de Fundo
        IMAGE_PATH = self.root + "images/back.jpg"
        WIDTH, HEIGTH = 850, 600
        bkrgframe = BkgrFrameWhats(self, IMAGE_PATH, WIDTH, HEIGTH)
        bkrgframe.pack()

        #Botão de Login no WhatsApp Web
        log_bt = ttk.Button(self,
                    text="Whatsapp Web", 
                    command = lambda: threading.Thread(target = self.f1, daemon = True).start())
        log_bt.place(relx=0.10,rely=0.12,relwidth=0.14,relheight=0.05, anchor='w')

        #Criação Listbox
        self.listbox = tk.Listbox(self, 
                        background='#163537',
                        relief='solid',
                        foreground='white',
                        font='segoe 11',
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

        #Caixa de Mensagem de Texto
        self.text_msg = tk.Text(self, 
                        fg="white", 
                        bg="#163537", 
                        font = "-family {Segoe UI} -size 16"
                            )
        self.text_msg.place(relx=0.43, rely=0.29, relwidth=0.55, relheight=0.30, anchor = 'w')
        self.scrollbar_text_msg_y = ttk.Scrollbar(self, orient="vertical")
        self.scrollbar_text_msg_y.config(command=self.text_msg.yview)
        self.scrollbar_text_msg_y.place(relx=0.97,rely=0.29, relwidth=0.015, relheight=0.30, anchor='w')
        self.text_msg.config(yscrollcommand=self.scrollbar_text_msg_y.set)

        #Caixa de Mensagem da Imagem
        self.text_img = tk.Text(self, 
                        fg="white", 
                        bg="#163537",
                        font = "-family {Segoe UI} -size 16"
                            )
        self.text_img.place(relx=0.43, rely=0.66, relwidth=0.55, relheight=0.30, anchor = 'w')
        self.scrollbar_text_img_y = ttk.Scrollbar(self, orient="vertical")
        self.scrollbar_text_img_y.config(command=self.text_img.yview)
        self.scrollbar_text_img_y.place(relx=0.97,rely=0.66, relwidth=0.015, relheight=0.30, anchor='w')
        self.text_img.config(yscrollcommand=self.scrollbar_text_img_y.set)
        
        #Botão para carregar Imagem ou Video
        img_or_video_bt = ttk.Button(self,
                    text="Imagem", 
                    command = lambda: threading.Thread(target = self.f3, daemon = True).start())
        img_or_video_bt.place(relx=0.55,rely=0.85,relwidth=0.08,relheight=0.05, anchor='w')
        #Botão para carregar Arquivo
        file_bt = ttk.Button(self,
                    text="Arquivo", 
                    command = lambda: threading.Thread(target = self.f4, daemon = True).start())
        file_bt.place(relx=0.64,rely=0.85,relwidth=0.08,relheight=0.05, anchor='w')

        #Botão para Limpar diretório da Imagem ou Video
        clear_img_or_video_bt = ttk.Button(self,
                    text="Apagar", 
                    command = lambda: threading.Thread(target = self.f5, daemon = True).start())
        clear_img_or_video_bt.place(relx=0.55,rely=0.905,relwidth=0.08,relheight=0.05, anchor='w')
        #Botão para carregar Arquivo
        clear_file_or_video_bt = ttk.Button(self,
                    text="Apagar", 
                    command = lambda: threading.Thread(target = self.f6, daemon = True).start())
        clear_file_or_video_bt.place(relx=0.64,rely=0.905,relwidth=0.08,relheight=0.05, anchor='w')

        #Botão para Enviar mensagens 
        send_bt = ttk.Button(self,
                    text="Enviar", 
                    command = lambda: threading.Thread(target = self.f7, daemon = True).start())
        send_bt.place(relx=0.46,rely=0.97,relwidth=0.08,relheight=0.05, anchor='w')

        #Barra de Progresso
        self.progress_bar = ttk.Progressbar(self, length= 80, mode = 'indeterminate')
        self.progress_bar.place(relx=0.55,rely=0.97,relwidth=0.44,relheight=0.05, anchor='w')

    def f1(self): whatsapp_login(self)

    def f2(self): load_contacts(self)

    def f3(self): load_img_or_video(self)

    def f4(self): load_doc(self)

    def f5(self): clear_img_path(self)

    def f6(self): clear_file_path(self)

    def f7(self): send_message(self)


def main():
    
    app = Geral()
    style = ttk.Style()  
    style.theme_use('scidgreen')
    style.configure('.', background='white')
    style.configure('my.TFrame', background='white', foreground ='black', font = "segoe 9 bold")
    style.configure('TRadiobutton', background="transparent", foreground='transparent', font = 'segoe 10 bold', justify='top', side='w')
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

    app.title("Whatsapp Bot")
    current_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0])) + "\\"

    app.wm_attributes('-alpha')
    app.iconbitmap("/".join(current_folder.split("\\")[0:-2]) + "/images/logo.ico")
    app.mainloop()

if __name__=="__main__":
    main()
