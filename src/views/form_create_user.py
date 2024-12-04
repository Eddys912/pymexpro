from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox
from src.controllers.user_controller import UserController


class FormCreate:
    def __init__(self, main_window):
        self.user_page = uic.loadUi("src/views/form_create_user.ui")
        self.user_page.show()
        self.user_controller = UserController()
        self.main_window = main_window
        self.user_page.btn_create_user.clicked.connect(self.form_create_user)

    def form_create_user(self):

        user_data = {
            "first_name": self.user_page.line_input_first_name.text().strip(),
            "last_name": self.user_page.line_input_last_name.text().strip(),
            "username": self.user_page.line_input_username.text().strip(),
            "birth_date": self.user_page.cb_birth_date.dateTime().toString(
                "yyyy-MM-dd HH:mm:ss"
            ),
            "gender": self.user_page.cb_sex.currentText(),
            "phone": self.user_page.line_input_phone.text().strip(),
            "role": self.user_page.cb_role.currentText(),
            "email": self.user_page.line_input_email.text().strip(),
            "address": self.user_page.line_input_address.text().strip(),
            "password": self.user_page.line_input_password.text().strip(),
        }

        if not self.validate_form_fields(user_data):
            return

        result = self.user_controller.create_user(user_data)

        if result["success"]:
            QMessageBox.information(self.user_page, "Éxito", result["message"])
            self.main_window.apply_filters()
            self.user_page.close()
        else:
            QMessageBox.warning(self.user_page, "Error", result["message"])

    def validate_form_fields(self, user_data):
        translations = {
            "first_name": "Nombre",
            "last_name": "Apellido",
            "username": "Usuario",
            "birth_date": "Fecha de nacimiento",
            "gender": "Sexo",
            "phone": "Telefono",
            "role": "Rol",
            "email": "Correo electrónico",
            "address": "Dirección",
            "password": "Contraseña",
        }
        for key, value in user_data.items():
            if not value:
                field_name = translations.get(key, key)
                QMessageBox.warning(
                    self.user_page,
                    "Error",
                    f"El campo '{field_name}' no puede estar vacío.",
                )
                return False

        if user_data["gender"] not in ["Decoracion", "Dormitorio"]:
            QMessageBox.warning(self.user_page, "Error", "Seleccione un género válido.")
            return False

        if user_data["role"] == "Seleccionar...":
            QMessageBox.warning(
                self.user_page, "Error", "Debe seleccionar un rol válido."
            )
            return False

        if not user_data["phone"].isdigit() or len(user_data["phone"]) != 1:
            QMessageBox.warning(
                self.user_page,
                "Error",
                "El número de teléfono debe contener exactamente 10 dígitos.",
            )
            return False

        return True
