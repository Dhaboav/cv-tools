import os
import sys
import xml.etree.ElementTree as ET


class XML2YOLO:
    def __init__(self, folder_path:str, class_mapping:dict):
        self.__xml_folder  = folder_path
        self.__classes     = class_mapping
        self.__output_path = 'runs/xml2yolo'
        os.makedirs(self.__output_path, exist_ok=True)
        self.__start_convert()

    # Core
    def __xml_yolo(self, xml, yolo):
        __tree = ET.parse(xml)
        __root = __tree.getroot()
        __image_width = int(__root.find('size/width').text)
        __image_height = int(__root.find('size/height').text)

        with open(yolo, 'w') as __write_yolo:
            for __obj in __root.findall('object'):
                __class_name = __obj.find('name').text
                if __class_name not in self.__classes:
                    continue

                __xmin = int(__obj.find('bndbox/xmin').text)
                __ymin = int(__obj.find('bndbox/ymin').text)
                __xmax = int(__obj.find('bndbox/xmax').text)
                __ymax = int(__obj.find('bndbox/ymax').text)

                # Yolo formating
                __x_center = (__xmin + __xmax) / (2.0 * __image_width)
                __y_center = (__ymin + __ymax) / (2.0 * __image_height)
                __width = (__xmax - __xmin) / __image_width
                __height = (__ymax - __ymin) / __image_height
                __write_yolo.write(f'{self.__classes[__class_name]} {__x_center} {__y_center} {__width} {__height}\n')
                
    def __start_convert(self):
        __progress_count = 0
        __total_xml = len(os.listdir(self.__xml_folder))
        for __xml_file in os.listdir(self.__xml_folder):
            if __xml_file.endswith('.xml'):
                __xml_path = os.path.join(self.__xml_folder, __xml_file)
                __save = os.path.join(self.__output_path, __xml_file.replace('.xml', '.txt'))
                self.__xml_yolo(__xml_path, __save)

                # Print out progress bar
                __progress_count += 1
                __progress = int((__progress_count / __total_xml) * 40)
                sys.stdout.write('\r[' + '.' * __progress + ' ' * (40 - __progress) + f'] {__progress_count}/{__total_xml-1}')
                sys.stdout.flush()