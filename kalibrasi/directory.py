import os
from tkinter import messagebox
import cv2 as cv
import numpy as np

class Dir:
    def __init__(self):
        pass
        
    def check_folder(self, output, folder_name):
            folder_path = os.path.join(output, folder_name)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                return folder_path

            count = 2
            while True:
                new_folder_name = f'{folder_name}{count}'
                new_folder_path = os.path.join(output, new_folder_name)
                if not os.path.exists(new_folder_path):
                    os.makedirs(new_folder_path)
                    return new_folder_path
                count += 1

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
            messagebox.showerror('Error', f'{e}')
            exit()

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
            messagebox.showerror('Error', f'{e}')
            return None, None
