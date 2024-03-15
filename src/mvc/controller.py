import sys
from pathlib import Path
from tkinter import messagebox

# Add the parent directory to the sys.path
current_folder = Path(__file__).resolve().parent
parent_folder = current_folder.parent
sys.path.append(str(parent_folder))

from mvc.model import Model
from etc.imgset import ImgSet
from etc.xml2img import XML2Img
from etc.yolo2img import YOLO2Img
from etc.xml2yolo import XML2YOLO
from etc.file_change import FileChange
from etc.name_dialog import NameDialog
from etc.capture_img import CaptureImg
from etc.color_picker import ColorPicker
from etc.custom_dialog import CustomDialog
from etc.single_dialog import SingleDialog


class Controller:
    def __init__(self):
        self.__model = Model()

    # Handling event GUI
    def handle_menu_button(self, choice:str):
        if choice == 'XML':
            custom_dialog = CustomDialog()
            custom_dialog.run()
            try:
                __paths = custom_dialog.paths
                if __paths:
                    XML2Img(__paths[0], __paths[1], self.__model.get_class_name(), self.__model.get_class_color(), self.__model.get_class_counter())
                    self.show_info_dialog('System Info', 'XML checking done')
            except AttributeError:
                self.show_error_dialog('System Error', 'No Folder Path!')
                
        elif choice == 'YOLO':
            custom_dialog = CustomDialog()
            custom_dialog.run()
            try:
                __paths = custom_dialog.paths
                if __paths:
                    YOLO2Img(__paths[0], __paths[1], self.__model.get_class_name(), 
                            self.__model.get_class_color(), self.__model.get_class_counter())
                
                    self.show_info_dialog('System Info', 'YOLO checking done')      
            except AttributeError:
                self.show_error_dialog('System Error', 'No Folder Path!')

        elif choice == 'XML2YOLO':
            single_dialog = SingleDialog()
            single_dialog.run()
            try:
                __path = single_dialog.paths
                if __path:
                    XML2YOLO(__path, self.__model.get_class_mapping())
                    self.show_info_dialog('System Info', 'XML2YOLO converting done')
            except AttributeError:
                self.show_error_dialog('System Error', 'No Folder Path!')
                
        elif choice == 'Imgsets':
            single_dialog = SingleDialog()
            single_dialog.run()
            try:
                __path = single_dialog.paths
                if __path:
                    __imgset = ImgSet(__path)
                    self.show_info_dialog('System Info', f'Done splitting {__imgset.total} labels')
            except AttributeError:
                self.show_error_dialog('System Error', 'No Folder Path!')

        elif choice == 'Capture':
            c = CaptureImg(self.__model.get_index(), (self.__model.get_width(), self.__model.get_height()))
            c.run()

        elif choice == 'Color':
            c= ColorPicker(self.__model.get_index(), (self.__model.get_width(), self.__model.get_height()))
            c.run()

        elif choice == 'Ubah':
            name_dialog = NameDialog()
            name_dialog.run()
            try:
                __path = name_dialog.paths
                if __path:
                    __file_changer = FileChange(__path[0]+'{}', __path[1])
                    __file_changer.run()
                    self.show_info_dialog('System Info', f'Done Changed {__file_changer.counter} files')
            except AttributeError:
                self.show_error_dialog('System Error', 'No Folder Path!')

    def show_info_dialog(self, title:str, message:str):
        messagebox.showinfo(title, message)

    def show_error_dialog(self, title:str, message:str):
        messagebox.showerror(title, message)