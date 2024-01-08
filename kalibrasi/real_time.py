import numpy as np
import os
import time
import cv2 as cv
import tkinter as tk
from tkinter import messagebox
from directory import Dir


class RealTime:
    def __init__(self, camera, chessboard_size, square_size):
        # GUI
        self.root = tk.Tk()
        self.root.withdraw()

        # Dir stuff
        self.output = os.path.join('runs', 'take_data')
        self.folder_name = 'kalibrasi'

        self.directory = Dir()
        self.base_folder_path = self.directory.check_folder(self.output, self.folder_name)
        self.interval = 3
        self.start_time = time.time()

        # Camera
        self.camera = cv.VideoCapture(camera, cv.CAP_DSHOW)
        if not self.camera.isOpened():
            messagebox.showerror('Error', 'Failed to open the camera. Exiting...')
            exit()

        # Chessboard stuff
        self.CHESSBOARD = (chessboard_size[0], chessboard_size[1]) # row * cols
        self.SQUARE_SIZE = square_size

        # Calibration stuff
        self.criteria = (cv.TermCriteria_EPS + cv.TermCriteria_MAX_ITER, 30, 0.001)
        self.objPoints, self.imgPoints = [], []
        self.mtx, self.dist = [], []
        self.objp = np.zeros((np.prod(self.CHESSBOARD), 3), np.float32)
        self.objp[:, :2] = np.indices(self.CHESSBOARD).T.reshape(-1, 2)
        self.objp *= self.SQUARE_SIZE    
        
    def detecting_chess_pattern(self, frame_size):
        self.capture_count = 0
        corner_subpix = None
        while True:
            _, frame = self.camera.read()
            resize = cv.resize(frame, (frame_size[0], frame_size[1]))
            output = resize.copy()
            gray = cv.cvtColor(output, cv.COLOR_BGR2GRAY)
            ret, corner = cv.findChessboardCorners(gray, self.CHESSBOARD, cv.CALIB_CB_ADAPTIVE_THRESH + cv.CALIB_CB_FAST_CHECK + cv.CALIB_CB_NORMALIZE_IMAGE)
            if ret:
                corner_subpix = cv.cornerSubPix(gray, corner, (11, 11), (-1, -1), self.criteria)
                cv.drawChessboardCorners(output, self.CHESSBOARD, corner_subpix, ret)

            cv.putText(output, f'ENTER: Capture({self.capture_count})', (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)
            cv.putText(output, f'X: Calibrate', (10, 45), cv.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)
            cv.putText(output, f'ESC: Exit', (10, 60), cv.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)
            cv.imshow('Real Time Calibration', output)

            # Key binds
            key = cv.waitKey(50) & 0xFF
            if (key == 13 or (time.time() - self.start_time) > self.interval) and ret:  # Enter
                self.imgPoints.append(corner_subpix)
                self.objPoints.append(self.objp)
                self.directory.save_img(resize, self.capture_count, self.base_folder_path)
                self.capture_count += 1

            if key == 120:  # X
                if messagebox.askyesno('Dialog', 'End capture and do calibration?'):
                    cv.destroyAllWindows()
                    break

            if key == 27:  # ESC
                if messagebox.askyesno('Dialog', 'Exit the program?'):
                    self.camera.release()
                    cv.destroyAllWindows()
                    exit()

        if len(self.imgPoints) > 0:
            # Compute camera parameters
            print('calibrateCamera() start')

            h, w = resize.shape[:2]
            
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
            self.camera.release()
            cv.destroyAllWindows()
            exit()
    

        self.camera.release()
        cv.destroyAllWindows()