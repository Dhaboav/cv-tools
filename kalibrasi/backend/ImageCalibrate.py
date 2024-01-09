import os
import glob
import numpy as np
import cv2 as cv
from .Storage import Dir
from frontend.Message import CustomPopup

class ImageCalibrate:
    def __init__(self, chessboard_size, square_size, folder_path):

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

        # path
        self.directory = Dir()
        self.folder_path = folder_path

        # Interface
        self.box = CustomPopup()
        
    def run(self):
        images = glob.glob(os.path.join(self.folder_path, '*[jpn]*g'))
        detection_names = []
        for file in images:
            img = cv.imread(file)
            gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

            # Find chessboard corners
            ret, corners = cv.findChessboardCorners(gray, self.CHESSBOARD, cv.CALIB_CB_ADAPTIVE_THRESH + cv.CALIB_CB_FAST_CHECK + cv.CALIB_CB_NORMALIZE_IMAGE)
            print(f"File: {file}, ret: {ret}")
            if ret:
                self.objPoints.append(self.objp)
                corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), self.criteria)
                self.imgPoints.append(corners2)
                img = cv.drawChessboardCorners(img, self.CHESSBOARD, corners2, ret)

                # Store the name of the image with successful detection
                _, name = os.path.split(file)
                detection_names.append(name)

        if len(self.imgPoints) > 0:
            cv.destroyAllWindows()
            self.box.info_popup('Calibration Start!')
            

            h, w = img.shape[:2]
            ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(self.objPoints, self.imgPoints, (w, h), None, None)
            self.directory.save_data_calibration(mtx, dist, self.folder_path)
            self.mtx = mtx
            self.dist = dist

            # Evaluation based on reprojection error
            mean_error = 0
            for i in range(len(self.objPoints)):
                image_points2, _ = cv.projectPoints(self.objPoints[i], rvecs[i], tvecs[i], self.mtx, self.dist)
                error = cv.norm(self.imgPoints[i], image_points2, cv.NORM_L2) / len(image_points2)
                mean_error += error

            self.box.info_popup(mean_error / len(self.objPoints))
        else:
            self.box.error_popup('No chessboard corner detected!')
            exit()

        cv.destroyAllWindows()
        self.directory.txt_list(self.folder_path, detection_names)
        self.box.info_popup('Done!')