import os
import sys
import glob
import shutil
import cv2 as cv
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET


class XML2Img:
    def __init__(self, dataset_path:str, label_path:str, class_names:list, 
                class_colors:list, class_counts:list):
        
        self.__dataset_path   = dataset_path
        self.__label_path     = label_path
        self.__output_path    = 'runs/xml'
        self.__image_counter  = 0
        self.__class_names    = class_names
        self.__class_colors   = class_colors
        self.__class_counts   = class_counts

        self.__create_directory()
        self.__label_to_image()

    # Directory Stuff
    def __create_directory(self):
        if os.path.exists(self.__output_path):
            shutil.rmtree(self.__output_path)
        os.makedirs(self.__output_path)
        
    def __write_label_image(self, image, result_image):
        __image_path = os.path.join(self.__output_path, os.path.basename(image))
        cv.imwrite(__image_path, result_image)

    def __no_label(self, missing_label):
        __txtfile = os.path.join(self.__output_path, 'no_label.txt')
        with open(__txtfile, 'a') as __file:
            __file.write('\n' + missing_label)

    def __bgr_to_rgb(self, bgr_color):
        return (bgr_color[2] / 255.0, bgr_color[1] / 255.0, bgr_color[0] / 255.0)

    def __class_plt(self):
        __class_colors_rgb = [self.__bgr_to_rgb(bgr_color) for bgr_color in self.__class_colors]
        plt.title(f"Class Distribution of {self.__total_image} Images")
        plt.bar(self.__class_names, self.__class_counts, color=__class_colors_rgb)
        __plt_file = os.path.join(self.__output_path, 'PlotClass')
        plt.savefig(__plt_file)

    # Core
    def __read_xml(self, xml_path:str):
        __tree = ET.parse(xml_path)
        __root = __tree.getroot()
        __size = __root.find('size')
        __width = int(__size.find('width').text)
        __height = int(__size.find('height').text)
        __boxes = []
        for __obj in __root.findall('object'):
            __name_of_class = __obj.find('name').text
            __id_of_class = self.__class_names.index(__name_of_class)
            __box = __obj.find('bndbox')
            __x_min = int(__box.find('xmin').text)
            __y_min = int(__box.find('ymin').text)
            __x_max = int(__box.find('xmax').text)
            __y_max = int(__box.find('ymax').text)
            __boxes.append((__id_of_class, __x_min, __y_min, __x_max, __y_max))

        return __width, __height, __boxes

    def __label_to_image(self):
        __data_path = os.path.join(self.__dataset_path, '*[jpn]*g')
        self.__total_image = len(glob.glob(__data_path))
    
        for __image_path in glob.glob(__data_path):
            __image_filename = os.path.basename(__image_path)
            __xml_file = os.path.join(self.__label_path, __image_filename[:-4] + '.xml')
            try:
                _, _, boxes = self.__read_xml(__xml_file)
                __image = cv.imread(__image_path)
                
                # Print out progress bar
                self.__image_counter += 1
                progress = int((self.__image_counter / self.__total_image) * 40)
                sys.stdout.write('\r[' + '.' * progress + ' ' * (40 - progress) + f'] {self.__image_counter}/{self.__total_image}')
                sys.stdout.flush()

                # Read info from label
                for box in boxes:
                    class_id, x_min, y_min, x_max, y_max = box
                    bounding_color = self.__class_colors[class_id]
                    cv.rectangle(__image, (x_min, y_min), (x_max, y_max), bounding_color, 2)
                    self.__class_counts[class_id] += 1

                self.__write_label_image(__image_path, __image)
                self.__class_plt()

            except FileNotFoundError:
                self.__no_label(__xml_file)
                continue