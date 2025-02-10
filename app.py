from src.mvc.controller import Controller
from src.mvc.view import View

if __name__ == "__main__":
    INTERFACE = View()
    INTERFACE.root.wait_window(INTERFACE.popup)
    CONTROL = Controller()
    CONTROL.handle_menu_button(INTERFACE.choice)
