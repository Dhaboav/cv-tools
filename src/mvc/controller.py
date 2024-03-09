import sys
from pathlib import Path

# Add the parent directory to the sys.path
current_folder = Path(__file__).resolve().parent
parent_folder = current_folder.parent
sys.path.append(str(parent_folder))

from mvc.view import View
from mvc.model import Model
from etc.custom_dialog import CustomDialog
from etc.xml2img import XML2Img


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
                    __data, __label = __paths
                    XML2Img(__data, __label, self.__model.get_class_name(), 
                            self.__model.get_class_color(), self.__model.get_class_counter())
                    self.__view.show_info_dialog('System Info', 'XML checking done')
            except AttributeError:
                self.__view.show_error_dialog('System Error', 'No Folder Path!')
                
        elif __result == 'yoloLabel':
            pass 
        elif __result == 'convert':
            pass
        elif __result == 'imgset':
            pass
        elif __result == 'capture':
            pass
        elif __result == 'color':
            pass