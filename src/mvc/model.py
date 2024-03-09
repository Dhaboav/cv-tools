class Model:
    def __init__(self) -> None:
        self.__menu = {
            '1':'xmlLabel',
            '2':'yoloLabel',
            '3':'convert',
            '4':'imgset',
            '5':'capture',
            '6':'color'
        }
        self.__class_name = ['ROBOT', 'BOLA', 'PENGHALANG', 'GAWANG']
        self.__class_color = [(0, 255, 0), (0, 140, 255), (0, 0, 255), (255, 0, 255)]
        self.__class_counter = [0, 0, 0, 0]
        self.__class_mapping = {'ROBOT':'0', 'BOLA':'1', 'PENGHALANG':'2', 'GAWANG':'3'}

    # Getter
    def get_menu(self, menu_id) -> str:
        return self.__menu.get(menu_id, None)
    
    def get_class_name(self) -> list:
        return self.__class_name
    
    def get_class_color(self) -> list:
        return self.__class_color
    
    def get_class_counter(self) -> list:
        return self.__class_counter
    
    def get_class_mapping(self) -> dict:
        return self.__class_mapping