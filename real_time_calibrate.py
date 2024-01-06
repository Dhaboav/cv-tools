import numpy as np
import cv2 as cv
import tkinter as tk
from tkinter import simpledialog, messagebox


class Calibrate:
    def __init__(self):
        # GUI
        self.root = tk.Tk()
        self.root.withdraw()
        self.set_chessboard()
        self.set_window_size()

        # Camera
        self.camera = cv.VideoCapture(0)
        if not self.camera.isOpened():
            messagebox.showerror('Error', 'Failed to open the camera. Exiting...')
            exit()

        # Calibration stuff
        self.criteria = (cv.TermCriteria_EPS + cv.TermCriteria_MAX_ITER, 30, 0.001)
        self.objPoints, self.imgPoints = [], []
        self.mtx, self.dist = [], []
        self.objp = np.zeros((np.prod(self.CHESSBOARD), 3), np.float32)
        self.objp[:, :2] = np.indices(self.CHESSBOARD).T.reshape(-1, 2)
        self.objp *= self.SQUARE_SIZE

    def set_chessboard(self):
        chess_row = simpledialog.askinteger('Input', 'Enter chess row:')
        chess_cols = simpledialog.askinteger('Input', 'Enter chess cols:')
        square_size = simpledialog.askinteger('Input', 'Enter the size of one side of a square(mm):')

        self.CHESSBOARD = (chess_row, chess_cols)
        self.SQUARE_SIZE = square_size
        

    def set_window_size(self):
        self.frame_width = simpledialog.askinteger('Input', 'Enter the width of the window:')
        self.frame_height = simpledialog.askinteger('Input', 'Enter the height of the window:')

    def detecting_chess_pattern(self):
        
        if messagebox.askyesno('AskYesNo', 'Do you want to load calibration data (K.csv, d.csv)?'):
            # Load calibration data
            self.mtx = np.loadtxt('K.csv', delimiter=',')
            self.dist = np.loadtxt('d.csv', delimiter=',')
            print("K = \n", self.mtx)
            print("d = ", self.dist.ravel())

        else:
            capture_count = 0
            corner_subpix = None
            while True:
                _, frame = self.camera.read()
                resize = cv.resize(frame, (self.frame_width, self.frame_height))
                print(resize.shape)
                gray = cv.cvtColor(resize, cv.COLOR_BGR2GRAY)
                ret, corner = cv.findChessboardCorners(gray, self.CHESSBOARD, cv.CALIB_CB_ADAPTIVE_THRESH + cv.CALIB_CB_FAST_CHECK + cv.CALIB_CB_NORMALIZE_IMAGE)
                if ret:
                    corner_subpix = cv.cornerSubPix(gray, corner, (11, 11), (-1, -1), self.criteria)
                    cv.drawChessboardCorners(resize, self.CHESSBOARD, corner_subpix, ret)

                cv.putText(resize, f'ENTER: Capture({capture_count})', (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 2)
                cv.putText(resize, f'X: Calibrate', (10, 45), cv.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 2)
                cv.putText(resize, f'ESC: Exit', (10, 60), cv.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 2)
                cv.imshow('Real Time Calibration', resize)

                # Key binds
                key = cv.waitKey(50) & 0xFF
                if key == 13 and ret:  # Enter
                    self.imgPoints.append(corner_subpix)
                    self.objPoints.append(self.objp)
                    capture_count += 1

                if key == 120:  # X
                    if messagebox.askyesno('AskYesNo', 'End capture and do calibration?'):
                        cv.destroyAllWindows()
                        break

                if key == 27:  # ESC
                    if messagebox.askyesno('AskYesNo', 'Exit the program?'):
                        self.camera.release()
                        cv.destroyAllWindows()
                        exit()

            if len(self.imgPoints) > 0:
                # Compute camera parameters
                print('calibrateCamera() start')

                h, w = resize.shape[:2]
                
                ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(self.objPoints, self.imgPoints, (w, h), None, None)
                np.savetxt("K.csv", mtx, delimiter=',', fmt="%0.14f")  # Save camera matrix
                np.savetxt("d.csv", dist, delimiter=',', fmt="%0.14f")  # Save distortion coefficients

                self.mtx = mtx
                self.dist = dist

                # Evaluation based on reprojection error
                mean_error = 0
                for i in range(len(self.objPoints)):
                    image_points2, _ = cv.projectPoints(self.objPoints[i], rvecs[i], tvecs[i], self.mtx, self.dist)
                    error = cv.norm(self.imgPoints[i], image_points2, cv.NORM_L2) / len(image_points2)
                    mean_error += error
                print("Total error: ", mean_error / len(self.objPoints))  # Close to 0 is desirable (not suitable for fisheye lens)
            else:
                print("No chessboard corner detected!")
        

        #Show undistorted images
        if self.mtx.any():
            while True:
                ret, frame = self.camera.read()
                resize = cv.resize(frame, (self.frame_width, self.frame_height))
                undistort_image = cv.undistort(resize, self.mtx, self.dist)
                cv.imshow('Original', resize)
                cv.imshow('Undistorted', undistort_image)
                c = cv.waitKey(50) & 0xFF
                if c == 27:  # ESC
                    break
        else:
            print("Camera matrix is empty.")


        self.camera.release()
        cv.destroyAllWindows()


def main(args=None):
    excute = Calibrate()
    excute.detecting_chess_pattern()


if __name__ == '__main__':
    main()