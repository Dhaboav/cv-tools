import tkinter as tk
from tkinter import messagebox


class View:
    def __init__(self, master, controller):
        self.__controller = controller
        self.__component(master=master)

    def __component(self, master):
        __label_frame = tk.LabelFrame(master=master, text='LABEL')
        __xml_button = tk.Button(
            master=__label_frame, text='XML', width=20, 
            foreground='white', background='blue', 
            command=lambda: self.__controller.handle_menu_button(menu_id='1')
        )
        __yolo_button = tk.Button(
            master=__label_frame, text='YOLO', width=20, 
            foreground='white', background='blue', 
            command=lambda: self.__controller.handle_menu_button(menu_id='2')
        )
        __convert_button = tk.Button(
            master=__label_frame, text='XML2YOLO', width=20, 
            foreground='white', background='blue', 
            command=lambda: self.__controller.handle_menu_button(menu_id='3')
        )
        __imgset_button = tk.Button(
            master=__label_frame, text='Img Set', width=20, 
            foreground='white', background='blue', 
            command=lambda: self.__controller.handle_menu_button(menu_id='4')
        )

        __cv_frame = tk.LabelFrame(master=master, text='CAMERA')
        __capture_button = tk.Button(
            master=__cv_frame, text='Capture', width=20, 
            foreground='white', background='blue', 
            command=lambda: self.__controller.handle_menu_button(menu_id='5')
        )
        __color_button = tk.Button(
            master=__cv_frame, text='Color Picker', width=20, 
            foreground='white', background='blue', 
            command=lambda: self.__controller.handle_menu_button(menu_id='6')
        )

        __label_frame.pack()
        __xml_button.pack()
        __yolo_button.pack(pady=5)
        __convert_button.pack()
        __imgset_button.pack(pady=5)

        __cv_frame.pack()
        __capture_button.pack()
        __color_button.pack(pady=5)

    def show_info_dialog(self, title:str, message:str):
        messagebox.showinfo(title, message)