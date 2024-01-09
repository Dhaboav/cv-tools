import tkinter.messagebox as msg
from frontend.Interface import ChoiceDialog
from backend.TrainRatio import TrainRatio
from backend.Convert import ConvertXML2YOLO


if __name__ == "__main__":
    tester = ChoiceDialog()
    tester.root.wait_window(tester.popup)
    choice = tester.choice
    folder_path = tester.input_path

    if choice == 'Konversi XML ke YOLO':
        if folder_path:
            class_mapping = {"0": "ROBOT", "1": "BOLA", "2": "PENGHALANG", "3": "GAWANG"}
            excute = ConvertXML2YOLO(folder_path=folder_path, class_mapping=class_mapping)
            excute.run()
        else:
            msg.showerror('Error', 'No Folder Path!')

    elif choice == 'Train Rasio SSD Mobilenet':
        if folder_path:
            excute = TrainRatio(folder_path=folder_path)
            excute.run()
        else:
            msg.showerror('Error', 'No Folder Path!')