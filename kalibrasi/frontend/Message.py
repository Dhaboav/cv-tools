from tkinter import messagebox 

class CustomPopup:
    def __init__(self) -> None:
        pass

    def error_popup(self, text):
        messagebox.showerror('Error', text)

    def info_popup(self, text):
        messagebox.showinfo('Info', text)

        