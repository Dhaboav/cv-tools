import tkinter.messagebox as msg
from frontend.Interface import ChoiceDialog
from backend.TrainRatio import TrainRatio


if __name__ == "__main__":
    tester = ChoiceDialog()
    tester.root.wait_window(tester.popup)
    choice = tester.choice
    folder_path = tester.input_path

    if choice:
        pass
    
    elif choice == 'Train Rasio SSD Mobilenet':
        if folder_path:
            excute = TrainRatio(folder_path=folder_path)
            excute.run()
        else:
            msg.showerror('Error', 'No Folder Path!')