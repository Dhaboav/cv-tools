from mvc.data import INDEX

class Model:
    def __init__(self) -> None:
        self.__class_name = ['ROBOT', 'BOLA', 'PENGHALANG', 'GAWANG']
        self.__class_color = [(0, 255, 0), (0, 140, 255), (0, 0, 255), (255, 0, 255)]
        self.__class_counter = [0, 0, 0, 0]
        self.__class_mapping = {'ROBOT':'0', 'BOLA':'1', 'PENGHALANG':'2', 'GAWANG':'3'}

        self.__index = INDEX
        self.__width = 640
        self.__height = 480

    # Getter
    def get_class_name(self) -> list:
        return self.__class_name
    
    def get_class_color(self) -> list:
        return self.__class_color
    
    def get_class_counter(self) -> list:
        return self.__class_counter
    
    def get_class_mapping(self) -> dict:
        return self.__class_mapping
    
    def get_index(self) -> int:
        return self.__index
    
    def get_width(self) -> int:
        return self.__width
    
    def get_height(self) -> int:
        return self.__height