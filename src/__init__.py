class Run:
    def __init__(self):
        from src.helpers import HelpersFunc as Hf
        from src.controllers import MainController

        email, password = Hf.input_login_gui()
        MainController(email, password)

