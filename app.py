import tkinter as tk
from src.mvc.controller import Controller

if __name__ == "__main__":
    root = tk.Tk()

    # Calculate the center of the screen
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = 160
    window_height = 240
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    # Set the position of the window to the center
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    root.resizable(width=False, height=False)
    run = Controller(master=root)
    root.mainloop()