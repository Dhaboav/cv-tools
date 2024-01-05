import cv2 as cv
import numpy as np
import os
import glob

class Calibrate:
    def __init__(self, chessboard_size, folder_path):
        # Chessboard
        self.CHESSBOARD = chessboard_size
        self.criteria = (cv.TermCriteria_EPS + cv.TermCriteria_MAX_ITER, 30, 0.001)
        self.objPoints = []
        self.imgPoints = []
        self.objp = np.zeros((1, self.CHESSBOARD[0] * self.CHESSBOARD[1], 3), np.float32)
        self.objp[0, :, :2] = np.mgrid[0:self.CHESSBOARD[0], 0:self.CHESSBOARD[1]].T.reshape(-1, 2)

        # path
        self.folder_path = os.path.join(folder_path, '*[jpn]*g')
        self.calibration_data_file = os.path.join(folder_path, 'calibration_data.yaml')
        self.output_txt_path = os.path.join(folder_path, 'success.txt')

    def save_calibration_data(self, mtx, dist):
        fs = cv.FileStorage(self.calibration_data_file, cv.FILE_STORAGE_WRITE)
        fs.write("camera_matrix", mtx)
        fs.write("distortion_coefficients", dist)
        fs.release()

    def write_successful_detection_names(self, successful_detection_names):
        with open(self.output_txt_path, 'w') as file:
            for name in successful_detection_names:
                file.write(name + '\n')

    def run(self):
        # Load
        images = glob.glob(self.folder_path)
        successful_detection_names = []
        for file in images:
            img = cv.imread(file)
            gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

            # Find chessboard corners
            ret, corners = cv.findChessboardCorners(gray, self.CHESSBOARD, cv.CALIB_CB_ADAPTIVE_THRESH + cv.CALIB_CB_FAST_CHECK + cv.CALIB_CB_NORMALIZE_IMAGE)
            if ret:
                self.objPoints.append(self.objp)
                corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), self.criteria)
                self.imgPoints.append(corners2)
                img = cv.drawChessboardCorners(img, self.CHESSBOARD, corners2, ret)

                # Store the name of the image with successful detection
                _, name = os.path.split(file)
                successful_detection_names.append(name)

                # Perform camera calibration for each successful detection
                h, w = img.shape[:2]
                ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(self.objPoints, self.imgPoints, (w, h), None, None)

                if ret:
                    self.save_calibration_data(mtx, dist)
                    
                else:
                    print('Calibrate Fail!')

            cv.imshow('result calibrate', img)
            cv.waitKey(100)

        cv.destroyAllWindows()
        self.write_successful_detection_names(successful_detection_names)
        print('Done!')