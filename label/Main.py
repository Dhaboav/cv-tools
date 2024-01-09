import tkinter.messagebox as msg
from frontend.Interface import ChoiceDialog
from backend.TrainRatio import TrainRatio
from backend.Convert import ConvertXML2YOLO
from backend.LabelXml import LabelCheckXML


if __name__ == "__main__":
    tester = ChoiceDialog()
    tester.root.wait_window(tester.popup)
    choice = tester.choice
    folder_path = tester.input_path

    if choice == 'Cek Label XML':
        if folder_path:

            # Untuk data class sesuai urutan dari saat melakukan labeling.
            class_name = ["ROBOT", "BOLA", "PENGHALANG", "GAWANG"]
            class_color = [(0, 255, 0), (0, 140, 255), (0, 0, 255), (255, 255, 255)]
            class_count = [0, 0, 0, 0]

            excute = LabelCheckXML(dataset_path=folder_path)
            # train_boolean --> True: Train, False: Val
            excute.run(train_boolean=True, class_name=class_name, class_color=class_color, class_counter=class_count)
        else:
            msg.showerror('Error', 'No Folder Path!')

    elif choice == 'Konversi XML ke YOLO':
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