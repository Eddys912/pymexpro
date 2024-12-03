from PyQt6 import uic
from src.models.user_model import UserModel
from src.controllers.login_controller import LoginController
from src.views.main_view import Main


class Login:
    def __init__(self):
        self.login = uic.loadUi("src/views/login.ui")
        self.login.line_user.setFocus()
        self.login.show()

        self.login_controller = LoginController()

        self.init()

    def init(self):
        self.login.btn_access.clicked.connect(self.validate_login_form)

    def validate_login_form(self):

        credentials_data = {
            "username_or_email": self.login.line_user.text().strip(),
            "password": self.login.line_password.text().strip(),
        }

        if not self.validate_username(credentials_data["username_or_email"]):
            return
        if not self.validate_password(credentials_data["password"]):
            return

        self.login.lb_error.setText("")

        res = self.login_controller.authenticate_user(credentials_data)

        if res.get("success"):
            self.main = Main()
            self.login.close()
        else:
            self.show_error(res["message"])

    def validate_username(self, username):
        import re

        pattern = r"^[a-zA-Z0-9._@]+$"

        if not username:
            self.show_error("El nombre de usuario no puede estar vacío.")
            self.login.line_user.setFocus()
            return False

        if not re.match(pattern, username):
            self.show_error("El nombre de usuario contiene caracteres no permitidos.")
            self.login.line_user.setFocus()
            return False
        return True

    def validate_password(self, password):
        if len(password) < 8:
            self.show_error("La contraseña debe tener al menos 8 caracteres.")
            self.login.line_password.setFocus()
            return False
        if not password:
            self.show_error("La contraseña no puede estar vacía.")
            self.login.line_password.setFocus()
            return False
        return True

    def show_error(self, message):
        self.login.lb_error.setText(message)
