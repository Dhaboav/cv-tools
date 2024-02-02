import tkinter.messagebox as msg
from frontend.Interface import ChoiceDialog
from backend.TakeImg import TakeImg
from backend.ColorSelector import Color
from backend.ChangeName import ChangeName
from variable import CAMERA_INDEX, CAMERA_WIDTH, CAMERA_HEIGHT, NAME_FORMATING


if __name__ == "__main__":
    tester = ChoiceDialog()
    tester.root.wait_window(tester.popup)
    choice = tester.choice
    folder_path = tester.input_path

    if choice == 'Ambil gambar':
        if folder_path:
            excute = TakeImg(camera_index=CAMERA_INDEX, camera_size=(CAMERA_WIDTH, CAMERA_HEIGHT), folder_path=folder_path)
            excute.run()
        else:
            msg.showerror('Error', 'No Folder Path!')

    elif choice == 'Pilih warna':
        excute = Color(camera=CAMERA_INDEX, width=CAMERA_WIDTH, height=CAMERA_HEIGHT)
        excute.run()

    elif choice == 'Ubah nama':
        if folder_path:
            # example of name format -> test-{}.jpg
            excute = ChangeName(folder_path=folder_path, name_format=NAME_FORMATING)
            excute.run()
        else:
            msg.showerror('Error', 'No Folder Path!')