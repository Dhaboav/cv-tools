import tkinter as tk
from tkinter import filedialog, messagebox


class SingleDialog:
    def __init__(self):
        self.custom_root = tk.Toplevel()
        self.custom_root.title("Data Selector")

        # Set in center
        screen_width = self.custom_root.winfo_screenwidth()
        screen_height = self.custom_root.winfo_screenheight()
        x = (screen_width - 200) // 2
        y = (screen_height - 200) // 2
        self.custom_root.geometry(f"260x80+{x}+{y}")
        self.custom_root.resizable(False, False)
        self.paths = None
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.custom_root, text="Select data:").grid(row=0)
        self.__entry_data_path = tk.Entry(self.custom_root)
        self.__entry_data_path.grid(row=0, column=1)
        self.__button_data_browse = tk.Button(
            self.custom_root, text="Browse", command=self.__select_folder
        )
        self.__button_data_browse.grid(row=0, column=2, padx=5)
        self.__button_ok = tk.Button(self.custom_root, text="OK", command=self.on_ok)
        self.__button_ok.grid(row=2, column=1, pady=10)

    def __select_folder(self):
        folder_path = filedialog.askdirectory(title="Select a folder")
        if folder_path:
            self.__entry_data_path.delete(0, tk.END)
            self.__entry_data_path.insert(tk.END, folder_path)

    def on_ok(self):
        __data_path = self.__entry_data_path.get()
        if not __data_path:
            self.__show_error_dialog("Path Error", "Please select folder of data")
            return

        self.paths = __data_path
        self.custom_root.destroy()

    def __show_error_dialog(self, title: str, message: str):
        messagebox.showerror(title, message)

    def run(self):
        self.custom_root.wait_window()
