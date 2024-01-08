import cv2 as cv
from directory import Dir


class Calibrate:
    def __init__(self, camera, width, height, path) -> None:
        # Camera
        self.camera = camera
        self.width = width
        self.height = height

        # Setting load
        self.directory = Dir()
        self.mtx, self.dist= self.directory.load_data_calibration(path)

    def run(self):
        cap = cv.VideoCapture(self.camera, cv.CAP_DSHOW)
        cap.set(3, self.width)
        cap.set(4, self.height)

        while(True):
            ret, frame = cap.read()
            undistort_image = cv.undistort(frame, self.mtx, self.dist)

            cv.imshow('undistort', undistort_image)
            c = cv.waitKey(50) & 0xFF
            if c==27: # ESC
                break