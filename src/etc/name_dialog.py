import tkinter as tk
from tkinter import filedialog, messagebox


class NameDialog:
    def __init__(self):
        self.custom_root = tk.Toplevel()
        self.custom_root.title("File changer")

        # Set in center
        screen_width = self.custom_root.winfo_screenwidth()
        screen_height = self.custom_root.winfo_screenheight()
        x = (screen_width - 200) // 2
        y = (screen_height - 200) // 2
        self.custom_root.geometry(f"280x100+{x}+{y}")
        self.custom_root.resizable(False, False)
        self.paths = None
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.custom_root, text="Enter a name:").grid(row=0, sticky=tk.W)
        tk.Label(self.custom_root, text="Select a folder:").grid(row=1, sticky=tk.W)

        self.__entry_name = tk.Entry(self.custom_root)
        self.__entry_name.grid(row=0, column=1)

        self.__entry_path = tk.Entry(self.custom_root)
        self.__entry_path.grid(row=1, column=1)

        self.__button_browse = tk.Button(
            self.custom_root, text="Browse", command=self.__select_folder
        )
        self.__button_browse.grid(row=1, column=2, padx=5)

        self.__button_ok = tk.Button(self.custom_root, text="OK", command=self.on_ok)
        self.__button_ok.grid(row=2, column=1, pady=10)

    def __select_folder(self):
        folder_path = filedialog.askdirectory(title="Select a folder")
        if folder_path:
            self.__entry_path.delete(0, tk.END)
            self.__entry_path.insert(tk.END, folder_path)

    def on_ok(self):
        __name = self.__entry_name.get()
        __folder_path = self.__entry_path.get()

        if not __name:
            self.__show_error_dialog("Path Error", "Please enter name format")
            return

        if not __folder_path:
            self.__show_error_dialog("Path Error", "Please select folder of label")
            return

        self.paths = (__name, __folder_path)
        self.custom_root.destroy()

    def __show_error_dialog(self, title: str, message: str):
        messagebox.showerror(title, message)

    def run(self):
        self.custom_root.wait_window()
