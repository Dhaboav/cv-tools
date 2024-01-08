import tkinter as tk
from tkinter import filedialog, messagebox 
from real_time import RealTime
from offline import Offline
from calibrate import Calibrate

class ChoiceDialog:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.title = "Kalibrasi"
        self.choices = ["Load data kalibrasi", "Kalibrasi real time", "Kalibrasi gambar"]
        self.result = None
        self.folder_path = None
        self.create_dialog()

    def create_dialog(self):
        self.dialog = tk.Toplevel(self.root)
        self.dialog.title(self.title)

        # Pop up in center
        screen_width = self.dialog.winfo_screenwidth()
        screen_height = self.dialog.winfo_screenheight()
        x = (screen_width - 200) // 2
        y = (screen_height - 200) // 2
        self.dialog.geometry(f"230x150+{x}+{y}")

        label = tk.Label(self.dialog, text="Pilih opsi operasi:")
        label.pack(pady=5)  # Add space above and below the label

        # button setting
        button_frame = tk.Frame(self.dialog)
        button_frame.pack()
        button_width = 20  # Set a common width for buttons

        for choice in self.choices:
            button = tk.Button(button_frame, text=choice, width=button_width, command=lambda c=choice: self.on_button_click(c))
            button.pack(pady=2)  # Add space between buttons

            # Bind mouse enter event for hover effect
            button.bind("<Enter>", lambda event, b=button: b.config(bg="green", fg="white"))
            # Bind mouse leave event for normal state
            button.bind("<Leave>", lambda event, b=button: b.config(bg="SystemButtonFace", fg="black"))

    def get_folder_path(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.folder_path = folder_path

    def on_button_click(self, choice):
        self.result = choice
        if choice == "Load data kalibrasi" or choice == "Kalibrasi gambar":
            self.get_folder_path()
        self.dialog.destroy()


if __name__ == "__main__":
    dialog = ChoiceDialog()
    dialog.root.wait_window(dialog.dialog)
    choice = dialog.result
    folder_path = dialog.folder_path

    if choice == "Load data kalibrasi":
        if folder_path is not None:
            excute = Calibrate(0, 640, 480, folder_path)
            excute.run()
        else:
            messagebox.showerror('Error', 'No Path found!')

    elif choice == "Kalibrasi real time":
        excute = RealTime(1, (7, 9), 23)
        excute.detecting_chess_pattern((640, 480))
        
    elif choice == "Kalibrasi gambar":
        if folder_path is not None:
            excute = Offline((7, 9), folder_path)
            excute.run()
        else:
            messagebox.showerror('Error', 'No Path found!')