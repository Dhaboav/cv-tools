import os
import sys
import glob
import shutil
import cv2 as cv
import matplotlib.pyplot as plt


class YOLO2Img:
    def __init__(self, dataset_path: str, label_path: str, class_names: list, class_colors: list, class_counts: list):
        self.__dataset_path   = dataset_path
        self.__label_path     = label_path
        self.__output_path    = 'runs/yolo'
        self.__image_counter  = 0
        self.__class_names    = class_names
        self.__class_colors   = class_colors
        self.__class_counts   = class_counts

        self.__create_directory()
        self.__label_to_image()

    def yolo_to_opencv(self, x, y, width, height, image_width, image_height):
        x_min, y_min = int((x - width / 2) * image_width), int((y - height / 2) * image_height)
        x_max, y_max = int((x + width / 2) * image_width), int((y + height / 2) * image_height)
        return x_min, y_min, x_max, y_max
    
    def __label_to_image(self):
        data_path = os.path.join(self.__dataset_path, '*[jpn]*g')
        self.total_image = len(glob.glob(data_path))
        for image in glob.glob( data_path):
            image_filename = os.path.basename(image)
            yolo_file = os.path.join(self.__label_path, image_filename[:-4] + '.txt')
            try:
                with open(yolo_file, "r") as label:
                    label_lines = label.readlines()
                    read_image = cv.imread(image)
                    image_width, image_height = read_image.shape[1], read_image.shape[0]

                    # Print out progress bar
                    self.__image_counter += 1
                    progress = int((self.__image_counter / self.total_image) * 40)
                    sys.stdout.write('\r[' + '.' * progress + ' ' * (40 - progress) + f'] {self.__image_counter}/{self.total_image}')
                    sys.stdout.flush()

                    for label_line in label_lines:
                        data = label_line.strip().split(" ")
                        class_id, x_coor, y_coor, width, height = (int(data[0]), float(data[1]), float(data[2]), float(data[3]),float(data[4]))
                        x_min, y_min, x_max, y_max = self.yolo_to_opencv(x_coor, y_coor, width, height, image_width, image_height)
                        bounding_color = self.__class_colors[class_id]
                        cv.rectangle(read_image, (x_min, y_min), (x_max, y_max), bounding_color, 2)
                        self.__class_counts[class_id] += 1

                    self.__write_label_image(image, read_image)
                    self.__class_plt()

            except FileNotFoundError:
                self.__no_label(yolo_file)
                continue

    # Override private methods from XML2Img
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
        plt.title(f"Class Distribution of {self.total_image} Images")
        plt.bar(self.__class_names, self.__class_counts, color=__class_colors_rgb)
        __plt_file = os.path.join(self.__output_path, 'PlotClass')
        plt.savefig(__plt_file)
