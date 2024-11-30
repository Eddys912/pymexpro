from PyQt6 import uic
from src.controllers.user_controller import UserController


class UserPage:
    def __init__(self):
        self.user_page = uic.loadUi("src/views/create_user.ui")
        self.user_page.show()
        self.user_page.btn_create_user.clicked.connect(self.create_user)

    def create_user(self):
        new_student = UserController()

        first_name = self.user_page.line_input_first_name.text().strip()
        last_name = self.user_page.line_input_last_name.text().strip()
        username = self.user_page.line_input_username.text().strip()
        email = self.user_page.line_input_email.text().strip()
        phone = self.user_page.line_input_phone.text().strip()

        new_student.create_user(first_name, last_name, username, email, phone)
