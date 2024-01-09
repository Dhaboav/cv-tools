from frontend.Interface import ChoiceDialog


if __name__ == "__main__":
    tester = ChoiceDialog()
    tester.root.wait_window(tester.popup)