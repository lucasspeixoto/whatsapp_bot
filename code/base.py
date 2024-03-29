# -*- coding: utf_8 -*-
#encoding: utf-8

import os
import sys
import threading
import tkinter as tk
import tkinter.font as font
import tkinter.messagebox
import webbrowser
import zipfile
from tkinter import ttk

from PIL import Image, ImageTk
from ttkthemes import themed_tk

from contacts.load_contacts import load_contacts
from files.clear_path import clear_file_path, clear_img_path
from files.load_file import load_doc, load_img_or_video
from robots.send_message import send_message
from robots.whatsapp_login import whatsapp_login


class Geral(themed_tk.ThemedTk):
    def __init__(self, *args, **kwargs):
        themed_tk.ThemedTk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side='top', fill='both', expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        menu = tk.Menu(container)

        windows = tk.Menu(menu, tearoff=0, bg='white',
                          activebackground='#163537')
        options = tk.Menu(menu, tearoff=0, bg='white',
                          activebackground='#163537')

        menu.add_cascade(menu=windows, underline=1, label='Início')
        menu.add_cascade(menu=options, underline=1, label='Opções')

        windows.add_command(label='Whatsapp',
                            command=lambda: threading.Thread(target=self.show_frame(Whatsapp), daemon=True).start())
        windows.add_command(label='Ajuda',
                            command=lambda: threading.Thread(target=self.show_url, daemon=True).start())

        options.add_command(label='Sair',
                            command=lambda: threading.Thread(target=self.quit, daemon=True).start())
        options.add_command(label='Observações',
                            command=lambda: threading.Thread(target=self.show_help, daemon=True).start())

        themed_tk.ThemedTk.config(self, menu=menu)

        frame = Whatsapp(parent=container, controller=self)
        self.frames[Whatsapp] = (frame, '850x600+0+0', 'normal')
        frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame(Whatsapp)

    def show_frame(self, cont):
        frame, geometry, state = self.frames[cont]
        self.update_idletasks()
        self.geometry(geometry)
        self.state(state)
        frame.tkraise()

    def show_url(self):
        url = '''https://www.figma.com/file/UogdkCEQURpOcCfYNZNHam/
        WhatsApp-Bot?node-id=0%3A1'''
        webbrowser.open(url)
        return

    def onexit():
        sys.exit(0)

    def show_help():
        text = '''Observações Importantes: \n
        ➣ .
        '''
        tkinter.messagebox.showinfo('Ajuda', text)


class BkgrFrameWhats(tk.Frame):
    def __init__(self, parent, file_path, width, height):
        super(BkgrFrameWhats, self).__init__(
            parent, borderwidth=0, highlightthickness=0)

        self.canvas = tk.Canvas(self, width=width, height=height)
        self.canvas.pack()

        pil_img = Image.open(file_path)
        self.img = ImageTk.PhotoImage(
            pil_img.resize((width, height), Image.ANTIALIAS))
        self.bg = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img)

        # Título
        self.canvas.create_text(5, 25,
                                text='WhatsApp Bot',
                                fill='white',
                                anchor='w',
                                font=('arial bold', 28)
                                )

        # Lista de Contatos
        self.canvas.create_text(5, 115,
                                text='Lista de Contatos',
                                fill='white',
                                anchor='w',
                                font=('arial bold', 20)
                                )

        # Caixa de Texto 1
        self.canvas.create_text(365, 65,
                                text='Mensagem de Texto',
                                fill='white',
                                anchor='w',
                                font=('arial bold', 20)
                                )

        # Caixa de Texto 2
        self.canvas.create_text(365, 285,
                                text='Mensagem de Imagem',
                                fill='white',
                                anchor='w',
                                font=('arial bold', 20)
                                )
        # Anexo
        self.canvas.create_text(365, 510,
                                text='Anexos',
                                fill='white',
                                anchor='w',
                                font=('arial bold', 20)
                                )

    def add(self, widget, x, y):
        canvas_window = self.canvas.create_window(
            x, y, anchor=tk.NW, window=widget)
        return widget


class Whatsapp(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.place(relheight=1, relwidth=1)

        # Fontes
        font.nametofont('TkTextFont').configure(size=12)
        font.nametofont('TkDefaultFont').configure(size=12)

        # Variáveis
        self.per = tk.StringVar()

        # Caminho Executável
        self.current_folder = os.path.dirname(os.path.abspath(__file__)) + '/'

        # Caminho Raiz
        if sys.platform in ["linux", 'linux2']:
            print('Sistema: LINUX')
            self.root = os.getcwd() + '/whatsapp_bot/'
        elif sys.platform == "win32":
            print('Sistema: WINDOWS')
            self.root = "/".join(self.current_folder.split("\\")
                                 [0:-1]) + '/'  # Local

        # Plano de Fundo
        image_path = self.root + 'assets/imgs/back.jpg'
        width, heigth = 850, 600
        bkrgframe = BkgrFrameWhats(self, image_path, width, heigth)
        bkrgframe.pack()

        # User Check
        try:
            os.remove(self.current_folder + 'users.txt')
        except FileNotFoundError:
            pass
        with zipfile.ZipFile(self.current_folder + 'users.zip', 'r') as zf:
            zf.extractall(self.current_folder, pwd=b'3010199110021994')
            with open(self.current_folder + 'users.txt', encoding='utf8') as f:
                users = [line.strip() for line in f]
                f.close()
                zf.close()
                os.remove(self.current_folder + 'users.txt')
        user = os.path.expanduser(os.getenv('USERPROFILE')).replace(
            '\\', '/').split('/')[-1]
        if user.lower() not in users:
            tkinter.messagebox.showerror('ERRO', 'Máquina não autorizada.')
            sys.exit(0)
        else:
            pass

        # Botão de Login no WhatsApp Web
        log_bt = ttk.Button(self,
                            text='Login',
                            style='login.TButton',
                            command=lambda: threading.Thread(target=self.f1, daemon=True).start())
        log_bt.place(relx=0.01, rely=0.12, relwidth=0.10,
                     relheight=0.05, anchor='w')

        # Criação Listbox
        self.listbox = tk.Listbox(self,
                                  background='#163537',
                                  relief='solid',
                                  foreground='white',
                                  font='segoe 11',
                                  selectmode='extended'
                                  )
        self.listbox.place(relx=0.005, rely=0.57,
                           relwidth=0.40, relheight=0.68, anchor='w')
        self.scrollbar_list_y = ttk.Scrollbar(self, orient='vertical')
        self.scrollbar_list_y.config(command=self.listbox.yview)
        self.scrollbar_list_y.place(
            relx=0.40, rely=0.57, relwidth=0.015, relheight=0.68, anchor='w')
        self.listbox.config(yscrollcommand=self.scrollbar_list_y.set)
        self.scrollbar_list_x = ttk.Scrollbar(self, orient='horizontal')
        self.scrollbar_list_x.config(command=self.listbox.xview)
        self.scrollbar_list_x.place(
            relx=0.005, rely=0.895, relwidth=0.395, relheight=0.025, anchor='w')
        self.listbox.config(xscrollcommand=self.scrollbar_list_x.set)

        # Botão para carregar contatos
        load_bt = ttk.Button(self,
                             text='Carregar',
                             command=lambda: threading.Thread(target=self.f2, daemon=True).start())
        load_bt.place(relx=0.005, rely=0.955, relwidth=0.10,
                      relheight=0.05, anchor='w')

        # Caixa de Mensagem de Texto
        self.text_msg = tk.Text(self,
                                fg='white',
                                bg='#163537',
                                font='-family {Segoe UI} -size 16'
                                )
        self.text_msg.place(relx=0.43, rely=0.29,
                            relwidth=0.55, relheight=0.30, anchor='w')
        self.scrollbar_text_msg_y = ttk.Scrollbar(self, orient='vertical')
        self.scrollbar_text_msg_y.config(command=self.text_msg.yview)
        self.scrollbar_text_msg_y.place(
            relx=0.97, rely=0.29, relwidth=0.015, relheight=0.30, anchor='w')
        self.text_msg.config(yscrollcommand=self.scrollbar_text_msg_y.set)

        # Caixa de Mensagem da Imagem
        self.text_img = tk.Text(self,
                                fg='white',
                                bg='#163537',
                                font='-family {Segoe UI} -size 16'
                                )
        self.text_img.place(relx=0.43, rely=0.66,
                            relwidth=0.55, relheight=0.30, anchor='w')
        self.scrollbar_text_img_y = ttk.Scrollbar(self, orient='vertical')
        self.scrollbar_text_img_y.config(command=self.text_img.yview)
        self.scrollbar_text_img_y.place(
            relx=0.97, rely=0.66, relwidth=0.015, relheight=0.30, anchor='w')
        self.text_img.config(yscrollcommand=self.scrollbar_text_img_y.set)

        # Botão para carregar Imagem ou Video
        img_or_video_bt = ttk.Button(self,
                                     text='Imagem',
                                     command=lambda: threading.Thread(target=self.f3, daemon=True).start())
        img_or_video_bt.place(relx=0.55, rely=0.85,
                              relwidth=0.08, relheight=0.05, anchor='w')
        # Botão para carregar Arquivo
        file_bt = ttk.Button(self,
                             text='Arquivo',
                             command=lambda: threading.Thread(target=self.f4, daemon=True).start())
        file_bt.place(relx=0.64, rely=0.85, relwidth=0.08,
                      relheight=0.05, anchor='w')

        # Botão para Limpar diretório da Imagem ou Video
        clear_img_or_video_bt = ttk.Button(self,
                                           text='Apagar',
                                           command=lambda: threading.Thread(target=self.f5, daemon=True).start())
        clear_img_or_video_bt.place(
            relx=0.55, rely=0.905, relwidth=0.08, relheight=0.05, anchor='w')

        # Botão para carregar Arquivo
        clear_file_or_video_bt = ttk.Button(self,
                                            text='Apagar',
                                            command=lambda: threading.Thread(target=self.f6, daemon=True).start())
        clear_file_or_video_bt.place(
            relx=0.64, rely=0.905, relwidth=0.08, relheight=0.05, anchor='w')

        # Botão para Enviar mensagens
        send_bt = ttk.Button(self,
                             text='Enviar',
                             command=lambda: threading.Thread(target=self.f7, daemon=True).start())
        send_bt.place(relx=0.46, rely=0.97, relwidth=0.08,
                      relheight=0.05, anchor='w')

        # Barra de Progresso
        self.progress_bar = ttk.Progressbar(
            self, length=80, mode='indeterminate')
        self.progress_bar.place(relx=0.55, rely=0.97,
                                relwidth=0.44, relheight=0.05, anchor='w')

    def f1(self): whatsapp_login(self)

    def f2(self): load_contacts(self)

    def f3(self): load_img_or_video(self)

    def f4(self): load_doc(self)

    def f5(self): clear_img_path(self)

    def f6(self): clear_file_path(self)

    def f7(self): send_message(self)


def main():

    app = Geral()

    app.title('Whatsapp Bot - v4.0.4')
    current_folder = os.path.dirname(os.path.abspath(__file__)) + '/'

    app.wm_attributes('-alpha')
    app.iconbitmap('/'.join(current_folder.split('\\')
                   [0:-1]) + '/assets/imgs/logo.ico')
    app.resizable(False, False)
    app.mainloop()


if __name__ == '__main__':
    main()
