from frontend.Interface import ChoiceDialog
from frontend.Message import CustomPopup
from backend.ImageCalibrate import ImageCalibrate
from backend.RealTimeCalibrate import RealTimeCalibrate
from backend.Test import Test
from variable import CAMERA_INDEX, CAMERA_WIDTH, CAMERA_HEIGHT, CHESSBOARD_SIZE, SQUARE_SIZE

if __name__ == "__main__":
    tester = ChoiceDialog()
    box = CustomPopup()
    tester.root.wait_window(tester.popup)
    choice = tester.choice
    folder_path = tester.input_path
    if choice == "Test Hasil Kalibrasi":
        if folder_path:
            excute = Test(camera=CAMERA_INDEX, width=CAMERA_WIDTH, height=CAMERA_HEIGHT, path=folder_path)
            excute.run()
            
    elif choice == "Kalibrasi real time":
        if folder_path:
            excute = RealTimeCalibrate(camera=CAMERA_INDEX, chessboard_size=CHESSBOARD_SIZE, square_size=SQUARE_SIZE, folder_path=folder_path)
            excute.detecting_chess_pattern(frame_size=(CAMERA_WIDTH, CAMERA_HEIGHT))
        else:
            box.error_popup("No folder path!")

    elif choice == "Kalibrasi gambar":
        if folder_path:
            excute = ImageCalibrate(chessboard_size=CHESSBOARD_SIZE, square_size=SQUARE_SIZE, folder_path=folder_path)
            excute.run()
        else:
            box.error_popup("No folder path!")