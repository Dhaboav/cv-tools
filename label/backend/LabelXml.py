import os
import sys
import glob
import shutil
import cv2 as cv
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET


class LabelCheckXML:
    def __init__(self, dataset_path, folder_name):
        self.dataset_path   = dataset_path
        self.output_path    = os.path.join(dataset_path, folder_name)
        self.image_counter  = 0
        self.create_output_directory()

    # Directory Stuff
    def create_output_directory(self):
        # Remove the existing directory if it exists
        if os.path.exists(self.output_path):
            shutil.rmtree(self.output_path)

        # Create a new directory
        os.makedirs(self.output_path)
        
    def write_label_image(self, image, result_image):
        image_path = os.path.join(self.output_path, os.path.basename(image))
        cv.imwrite(image_path, result_image)

    def no_label(self, missing_label):
        log_file = os.path.join(self.output_path, 'NoLabel.txt')
        with open(log_file, 'a') as file:
            file.write('\n' + missing_label)
    # ==============================================================================

    # Class Stuff     
    def class_data(self, class_name, class_color, class_count):
        self.class_names    = class_name
        self.class_colors   = class_color
        self.class_counts   = class_count

    def bgr_to_rgb(self, bgr_color):
        return (bgr_color[2] / 255.0, bgr_color[1] / 255.0, bgr_color[0] / 255.0)

    def class_plt(self, total, class_name, class_number, class_color):
        class_colors_rgb = [self.bgr_to_rgb(bgr_color) for bgr_color in class_color]
        
        plt.title(f"Class Distribution of {total} Images")
        bars = plt.bar(class_name, class_number, color=class_colors_rgb)
        plt_file = os.path.join(self.output_path, 'PlotClass')
        plt.savefig(plt_file)
    # ==============================================================================

    # Core
    def read_xml(self, xml_path):
        tree = ET.parse(xml_path)
        root = tree.getroot()
        size = root.find('size')
        image_width = int(size.find('width').text)
        image_height = int(size.find('height').text)
        boxes = []
        for obj in root.findall('object'):
            name_of_class = obj.find('name').text
            id_of_class = self.class_names.index(name_of_class)
            box = obj.find('bndbox')
            x_min = int(box.find('xmin').text)
            y_min = int(box.find('ymin').text)
            x_max = int(box.find('xmax').text)
            y_max = int(box.find('ymax').text)
            boxes.append((id_of_class, x_min, y_min, x_max, y_max))

        return image_width, image_height, boxes

    def label_to_image(self):
        data_path = os.path.join(self.dataset_path, 'images', '*[jpn]*g')
        self.total_image = len(glob.glob(data_path))
        for image in glob.glob(data_path):
            xml_file = image.replace('images', 'labels').replace(os.path.splitext(image)[1], '.xml')
            try:
                image_width, image_height, boxes = self.read_xml(xml_file)
                read_image = cv.imread(image)
                
                # Print out progress bar
                self.image_counter += 1
                progress = int((self.image_counter / self.total_image) * 40)
                sys.stdout.write('\r[' + '.' * progress + ' ' * (40 - progress) + f'] {self.image_counter}/{self.total_image}')
                sys.stdout.flush()

                # Read info from label
                for box in boxes:
                    class_id, x_min, y_min, x_max, y_max = box
                    bounding_color = self.class_colors[class_id]
                    cv.rectangle(read_image, (x_min, y_min), (x_max, y_max), bounding_color, 2)
                    self.class_counts[class_id] += 1

                self.write_label_image(image, read_image)
                self.class_plt(self.image_counter, self.class_names, self.class_counts, self.class_colors)

            except FileNotFoundError:
                self.no_label(xml_file)
                continue
    # ==============================================================================

    def run(self, class_name, class_color, class_counter):
        self.class_data(class_name, class_color, class_counter)
        self.label_to_image()