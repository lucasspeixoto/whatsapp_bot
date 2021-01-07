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

class Geral(themed_tk.ThemedTk):
    def __init__(self, *args, **kwargs):
        themed_tk.ThemedTk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        menu = tk.Menu(container)
        
        windows = tk.Menu(menu, tearoff=0, bg='white',activebackground='#50b66b')
        options = tk.Menu(menu, tearoff=0, bg='white',activebackground='#50b66b')

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

        for Frame, geometry, state in zip((Whatsapp, Ajuda), ('700x600+0+0', '700x600+0+0'), ('normal', 'normal')):
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
