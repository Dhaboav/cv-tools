import os
import cv2 as cv
import numpy as np
from frontend.Message import CustomPopup

class Dir:
    def __init__(self):
        self.box = CustomPopup()
        pass

    def save_img(self, img, capture_count, folder_path):
        file_name = f'image-{capture_count}.jpg'
        save_img = os.path.join(folder_path, file_name)
        cv.imwrite(save_img, img)

    def save_data_calibration(self, mtx, dist, folder_path):
        mtx_file_path = os.path.join(folder_path, 'mtx.csv')
        dist_file_path = os.path.join(folder_path, 'dist.csv')
        try:
            np.savetxt(mtx_file_path, mtx, delimiter=',', fmt="%0.14f")
            np.savetxt(dist_file_path, dist, delimiter=',', fmt="%0.14f")
        except Exception as e:
            self.box.error_popup(f'{e}')
            exit()

    def txt_list(self, folder_path, detection_names):
        txt_path = os.path.join(folder_path, 'ImageName.txt')
        with open(txt_path, 'w') as file:
            for name in detection_names:
                file.write(name + '\n')

    def load_data_calibration(self, path):
        camera_mat_file = os.path.join(path, 'mtx.csv')
        dist_coef_file = os.path.join(path, 'dist.csv')
        try:
            if os.path.exists(camera_mat_file) and os.path.exists(dist_coef_file):
                mtx = np.loadtxt(camera_mat_file, delimiter=',')
                dist = np.loadtxt(dist_coef_file, delimiter=',')
                return mtx, dist
            else:
                raise FileNotFoundError("Calibration files not found.")
            
        except Exception as e:
            self.box.error_popup(f'{e}')
            return None, None