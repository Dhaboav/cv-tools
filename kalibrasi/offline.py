from tkinter import messagebox
from directory import Dir
import cv2 as cv
import numpy as np
import os
import glob

class Offline:
    def __init__(self, chessboard_size, input_folder_path):
        # Chessboard
        self.CHESSBOARD = chessboard_size
        self.criteria = (cv.TermCriteria_EPS + cv.TermCriteria_MAX_ITER, 30, 0.001)
        self.objPoints, self.imgPoints  = [], []
        self.mtx, self.dist = [], []
        self.objp = np.zeros((1, self.CHESSBOARD[0] * self.CHESSBOARD[1], 3), np.float32)
        self.objp[0, :, :2] = np.mgrid[0:self.CHESSBOARD[0], 0:self.CHESSBOARD[1]].T.reshape(-1, 2)

        # path
        self.output = os.path.join('runs', 'take_data')
        self.folder_name = 'kalibrasi'
        self.directory = Dir()
        self.base_folder_path = self.directory.check_folder(self.output, self.folder_name)
        self.input_folder_path = os.path.join(input_folder_path, '*[jpn]*g')
        self.output_txt_path = os.path.join(self.base_folder_path, 'success.txt')

    def write_successful_detection_names(self, successful_detection_names):
        with open(self.output_txt_path, 'w') as file:
            for name in successful_detection_names:
                file.write(name + '\n')

    def run(self):
        # Load
        images = glob.glob(self.input_folder_path)
        successful_detection_names = []
        for file in images:
            img = cv.imread(file)
            gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

            # Find chessboard corners
            ret, corners = cv.findChessboardCorners(gray, self.CHESSBOARD, flags=cv.CALIB_CB_ADAPTIVE_THRESH + cv.CALIB_CB_FAST_CHECK + cv.CALIB_CB_NORMALIZE_IMAGE)
            if ret:
                self.objPoints.append(self.objp)
                corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), self.criteria)
                self.imgPoints.append(corners2)
                img = cv.drawChessboardCorners(img, self.CHESSBOARD, corners2, ret)

                # Store the name of the image with successful detection
                _, name = os.path.split(file)
                successful_detection_names.append(name)
            cv.imshow('result calibrate', img)
            cv.waitKey(100)

        if len(self.imgPoints) > 0:
            cv.destroyAllWindows()
            messagebox.showinfo('Info', 'Start calibration!')

            h, w = img.shape[:2]
            ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(self.objPoints, self.imgPoints, (w, h), None, None)
            self.directory.save_data_calibration(mtx, dist, self.base_folder_path)
            self.mtx = mtx
            self.dist = dist

            # Evaluation based on reprojection error
            mean_error = 0
            for i in range(len(self.objPoints)):
                image_points2, _ = cv.projectPoints(self.objPoints[i], rvecs[i], tvecs[i], self.mtx, self.dist)
                error = cv.norm(self.imgPoints[i], image_points2, cv.NORM_L2) / len(image_points2)
                mean_error += error

            messagebox.showinfo('Total Error', mean_error / len(self.objPoints))
        else:
            messagebox.showerror('Error', 'No chessboard corner detected!')
            exit()

        cv.destroyAllWindows()
        self.write_successful_detection_names(successful_detection_names)
        print('Done!')