from PyQt6 import uic
from src.models.user_model import UserModel
from src.controllers.user_controller import UserController
from src.views.main import Main


class Login:
    def __init__(self):
        self.login = uic.loadUi("src/views/login.ui")
        self.login.show()
        self.init()

    def init(self):
        self.login.btn_access.clicked.connect(self.validate_login)

    def validate_login(self):
        username = self.login.line_user.text().strip()
        password = self.login.line_password.text().strip()

        if not username:
            self.show_error("El nombre de usuario no puede estar vacío.")
            self.login.line_user.setFocus()
            return

        if not self.is_valid_username(username):
            self.show_error("El nombre de usuario contiene caracteres no permitidos.")
            self.login.line_user.setFocus()
            return

        if not password:
            self.show_error("La contraseña no puede estar vacía.")
            self.login.line_password.setFocus()
            return

        self.login.lb_error.setText("")

        user = UserModel(user=username, password=password)
        user_controller = UserController()
        res = user_controller.login(user)
        if res:
            print("Login correcto")
            self.main = Main()  # Crear la instancia de Main
            self.login.close()
        else:
            self.show_error("Usuario o contraseña incorrecta.")

    def is_valid_username(self, username):
        import re
        pattern = r"^[a-zA-Z0-9._@]+$"
        return bool(re.match(pattern, username))

    def show_error(self, message):
        self.login.lb_error.setText(message)
