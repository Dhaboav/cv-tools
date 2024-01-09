import tkinter.messagebox as msg
from frontend.Interface import ChoiceDialog
from backend.TakeImg import TakeImg
from backend.ColorSelector import Color
from backend.ChangeName import ChangeName


if __name__ == "__main__":
    tester = ChoiceDialog()
    tester.root.wait_window(tester.popup)
    choice = tester.choice
    folder_path = tester.input_path

    if choice == 'Ambil gambar':
        if folder_path:
            excute = TakeImg(camera_index=0, camera_size=(640,480), folder_path=folder_path)
            excute.run()
        else:
            msg.showerror('Error', 'No Folder Path!')

    elif choice == 'Pilih warna':
        excute = Color(0, 640, 480)
        excute.run()

    elif choice == 'Ubah nama':
        if folder_path:
            # example of name format -> test-{}.jpg
            excute = ChangeName(folder_path=folder_path, name_format='test-{}.jpg')
            excute.run()
        else:
            msg.showerror('Error', 'No Folder Path!')