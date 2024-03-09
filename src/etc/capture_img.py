import cv2 as cv
import os
import time


class CaptureImg:
    def __init__(self, camera_index, camera_size):
        self.camera_index = camera_index
        self.width = camera_size[0]
        self.height = camera_size[1]

        self.folder_path = 'runs/capture'
        self.capture_count = 0
        
        self.interval = 5
        self.start_time = time.time()
        
    def save_img(self, img):
        file_name = f'img-{self.capture_count}.jpg'
        save_img = os.path.join(self.folder_path, file_name)
        cv.imwrite(save_img, img)
        self.capture_count += 1

    def run(self):
        camera = cv.VideoCapture(self.camera_index, cv.CAP_DSHOW)
        camera.set(3, self.width)
        camera.set(4, self.height)
        camera.set(cv.CAP_PROP_AUTOFOCUS, 0)

        while True:
            ret, frame = camera.read()
            if not ret:
                break

            output = frame.copy()
            cv.putText(output, f'ENTER: capture({self.capture_count})', (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)
            cv.putText(output, f'ESC: Exit', (10, 60), cv.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)
            cv.imshow('Take', output)

            key = cv.waitKey(1) & 0xFF
            if (key == 13 or (time.time() - self.start_time) > self.interval): # Enter
                self.save_img(frame)
                self.start_time = time.time()
            
            if key == 27:  # ESC
                camera.release()
                cv.destroyWindow('Take')
                break