import xml.etree.ElementTree as ET
import os
import sys


class ConvertXML2YOLO:
    def __init__(self, folder_path, class_mapping):
        self.xml_folder  = folder_path
        self.classes     = class_mapping
        self.output_path = os.path.join(folder_path, 'Convert')
        os.makedirs(self.output_path, exist_ok=True)

    # ==============================================================================

    # Core
    def xml_to_yolo(self, xml, yolo):
        tree = ET.parse(xml)
        root = tree.getroot()
        image_width = int(root.find('size/width').text)
        image_height = int(root.find('size/height').text)

        with open(yolo, 'w') as write_yolo:
            for obj in root.findall('object'):
                class_name = obj.find('name').text
                if class_name not in self.classes:
                    continue

                xmin = int(obj.find('bndbox/xmin').text)
                ymin = int(obj.find('bndbox/ymin').text)
                xmax = int(obj.find('bndbox/xmax').text)
                ymax = int(obj.find('bndbox/ymax').text)

                # Yolo formating
                x_center = (xmin + xmax) / (2.0 * image_width)
                y_center = (ymin + ymax) / (2.0 * image_height)
                width = (xmax - xmin) / image_width
                height = (ymax - ymin) / image_height

                print(f"Class: {class_name}, YOLO: {self.classes[class_name]} {x_center} {y_center} {width} {height}")
                write_yolo.write(f'{self.classes[class_name]} {x_center} {y_center} {width} {height}\n')
    # ==============================================================================
                
    def run(self):
        progress_count = 0
        total_xml = len(os.listdir(self.xml_folder))
        for xml_file in os.listdir(self.xml_folder):
            if xml_file.endswith('.xml'):
                xml_path = os.path.join(self.xml_folder, xml_file)
                save = os.path.join(self.output_path, xml_file.replace('.xml', '.txt'))
                self.xml_to_yolo(xml_path, save)

                # Print out progress bar
                progress_count += 1
                progress = int((progress_count / total_xml) * 40)
                sys.stdout.write('\r[' + '.' * progress + ' ' * (40 - progress) + f'] {progress_count}/{total_xml-1}')
                sys.stdout.flush()