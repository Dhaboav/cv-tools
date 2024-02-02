import tkinter.messagebox as msg
from frontend.Interface import ChoiceDialog
from backend.TrainRatio import TrainRatio
from backend.Convert import ConvertXML2YOLO
from backend.LabelXml import LabelCheckXML
from backend.LabelYolo import LabelCheckYOLO
from variable import CLASSES_NAME, CLASSES_COLOR, CLASSES_COUNTER, CLASSES_MAPPING

def run_label_checker(checker, dataset_path, folder_name, class_name, class_color, class_counter):
    if dataset_path:
        checker_instance = checker(dataset_path=dataset_path, folder_name=folder_name)
        checker_instance.run(class_name=class_name, class_color=class_color, class_counter=class_counter)
    else:
        msg.showerror('Error', 'No Folder Path!')

def run_xml_to_yolo_converter(folder_path, class_mapping):
    if folder_path:
        converter_instance = ConvertXML2YOLO(folder_path=folder_path, class_mapping=class_mapping)
        converter_instance.run()
    else:
        msg.showerror('Error', 'No Folder Path!')

def run_train_ratio(folder_path):
    if folder_path:
        trainer_instance = TrainRatio(folder_path=folder_path)
        trainer_instance.run()
    else:
        msg.showerror('Error', 'No Folder Path!')


if __name__ == "__main__":
    INTERFACE = ChoiceDialog()
    INTERFACE.root.wait_window(INTERFACE.popup)
    FOLDER_PATH = INTERFACE.input_path

    if INTERFACE.choice == 'Cek Label XML':
        run_label_checker(LabelCheckXML, FOLDER_PATH, 'labelXML', CLASSES_NAME, CLASSES_COLOR, CLASSES_COUNTER)
    elif INTERFACE.choice == 'Cek Label YOLO':
        run_label_checker(LabelCheckYOLO, FOLDER_PATH, 'labelYOLO', CLASSES_NAME, CLASSES_COLOR, CLASSES_COUNTER)
    elif INTERFACE.choice == 'Konversi XML ke YOLO':
        run_xml_to_yolo_converter(FOLDER_PATH, CLASSES_MAPPING)
    elif INTERFACE.choice == 'Train Rasio SSD Mobilenet':
        run_train_ratio(FOLDER_PATH)