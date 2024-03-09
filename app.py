from src.mvc.view import View
from src.mvc.controller import Controller


if __name__ == "__main__":
    INTERFACE = View()
    INTERFACE.root.wait_window(INTERFACE.popup)
    CONTROL = Controller()
    CONTROL.handle_menu_button(INTERFACE.choice)