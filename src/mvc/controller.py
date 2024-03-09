import sys
from pathlib import Path

# Add the parent directory to the sys.path
current_folder = Path(__file__).resolve().parent
parent_folder = current_folder.parent
sys.path.append(str(parent_folder))

from mvc.view import View
from mvc.model import Model
from etc.imgset import ImgSet
from etc.xml2img import XML2Img
from etc.yolo2img import YOLO2Img
from etc.xml2yolo import XML2YOLO
from etc.capture_img import CaptureImg
from etc.color_picker import ColorPicker
from etc.custom_dialog import CustomDialog
from etc.single_dialog import SingleDialog


class Controller:
    def __init__(self, master):
        self.__model = Model()
        self.__master = master
        self.__view = View(master=self.__master, controller=self)

    # Handling event GUI
    def handle_menu_button(self, menu_id:str):
        __result = self.__model.get_menu(menu_id)
        if __result == 'xmlLabel':
            __popup = CustomDialog(root=self.__master)
            try:
                __paths = __popup.paths
                if __paths:
                    XML2Img(__paths[0], __paths[1], self.__model.get_class_name(), self.__model.get_class_color(), self.__model.get_class_counter())
                    self.__view.show_info_dialog('System Info', 'XML checking done')
            except AttributeError:
                self.__view.show_error_dialog('System Error', 'No Folder Path!')
                
        elif __result == 'yoloLabel':
            __popup = CustomDialog(root=self.__master)
            try:
                __paths = __popup.paths
                if __paths:
                    YOLO2Img(__paths[0], __paths[1], self.__model.get_class_name(), 
                            self.__model.get_class_color(), self.__model.get_class_counter())
                
                    self.__view.show_info_dialog('System Info', 'YOLO checking done')      
            except AttributeError:
                self.__view.show_error_dialog('System Error', 'No Folder Path!')

        elif __result == 'convert':
            __popup = SingleDialog(root=self.__master)
            try:
                __path = __popup.paths
                if __path:
                    XML2YOLO(__path, self.__model.get_class_mapping())
                    self.__view.show_info_dialog('System Info', 'XML2YOLO converting done')
            except AttributeError:
                self.__view.show_error_dialog('System Error', 'No Folder Path!')
                
        elif __result == 'imgset':
            __popup = SingleDialog(root=self.__master)
            try:
                __path = __popup.paths
                if __path:
                    __imgset = ImgSet(__path)
                    self.__view.show_info_dialog('System Info', f'Done spliting {__imgset.total} labels')
            except AttributeError:
                self.__view.show_error_dialog('System Error', 'No Folder Path!')

        elif __result == 'capture':
            CaptureImg(self.__model.get_index(), (self.__model.get_width(), self.__model.get_height()))

        elif __result == 'color':
            ColorPicker(self.__model.get_index(), (self.__model.get_width(), self.__model.get_height()))