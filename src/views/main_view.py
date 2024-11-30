from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox


class Main:
    def __init__(self):
        self.main = uic.loadUi("src/views/main_view.ui")
        self.main.show()
