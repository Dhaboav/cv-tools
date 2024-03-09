import tkinter as tk
import tkinter.simpledialog as simpledialog
from tkinter import messagebox, filedialog


class SingleDialog(simpledialog.Dialog):
    def __init__(self, root):
        self.custom_root = root
        super().__init__(self.custom_root)

    def body(self, master):
        tk.Label(master, text='Select data:').grid(row=0)

        self.__entry_data_path = tk.Entry(master)
        self.__entry_data_path.grid(row=0, column=1)

        self.__button_data_browse = tk.Button(master, text="Browse", command=self.__select_folder)
        self.__button_data_browse.grid(row=0, column=2, padx=5)

    def __select_folder(self):
        folder_path = filedialog.askdirectory(title="Select a folder")
        if folder_path:
            self.__entry_data_path.delete(0, tk.END)
            self.__entry_data_path.insert(tk.END, folder_path)

    def apply(self):
        __data_path = self.__entry_data_path.get()
        if not __data_path:
            self.__show_error_dialog('Path Error', 'Please select folder of data')
            return
        
        self.paths = (__data_path)
    
    def __show_error_dialog(self, title:str, message:str):
        messagebox.showerror(title, message)