from frontend.Interface import ChoiceDialog
from frontend.Message import CustomPopup
from backend.ImageCalibrate import ImageCalibrate
from backend.RealTimeCalibrate import RealTimeCalibrate
from backend.Test import Test

if __name__ == "__main__":
    tester = ChoiceDialog()
    box = CustomPopup()
    tester.root.wait_window(tester.popup)
    choice = tester.choice
    folder_path = tester.input_path
    if choice == "Test Hasil Kalibrasi":
        if folder_path:
            excute = Test(0, 640, 480, folder_path)
            excute.run()
            
    elif choice == "Kalibrasi real time":
        if folder_path:
            excute = RealTimeCalibrate(0, (7,9), 23, folder_path=folder_path)
            excute.detecting_chess_pattern((640, 480))
        else:
            box.error_popup("No folder path!")

    elif choice == "Kalibrasi gambar":
        if folder_path:
            excute = ImageCalibrate(chessboard_size=(7, 9), square_size=23, folder_path=folder_path)
            excute.run()
        else:
            box.error_popup("No folder path!")