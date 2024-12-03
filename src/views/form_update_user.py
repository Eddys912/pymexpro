from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox
from src.controllers.user_controller import UserController


class FormUpdate:
    def __init__(self, main_window, user_data):
        self.user_page = uic.loadUi("src/views/form_update_user.ui")
        self.user_page.show()
        self.user_controller = UserController()
        self.main_window = main_window
        self.user_data = user_data

        self.user_page.btn_update_user.clicked.connect(self.form_create_user)

    def set_values(self, user_data):
        self.user_page.line_input_first_name.setText(user_data["first_name"])
        self.user_page.line_input_last_name.setText(user_data["last_name"])
        self.user_page.line_input_username.setText(user_data["username"])
        self.user_page.cb_birth_date.setDateTime(user_data["birth_date"])
        self.user_page.cb_sex.setCurrentText(user_data["gender"])
        self.user_page.line_input_phone.setText(user_data["phone"])
        self.user_page.cb_role.setCurrentText(user_data["role"])
        self.user_page.line_input_email.setText(user_data["email"])
        self.user_page.line_input_address.setText(user_data["address"])

        is_active_text = "Activo" if user_data["is_active"] == 1 else "Inactivo"
        self.user_page.cb_status.setCurrentText(is_active_text)

    def form_create_user(self):
        user_data = {
            "user_id": self.user_data["user_id"],
            "first_name": self.user_page.line_input_first_name.text().strip(),
            "last_name": self.user_page.line_input_last_name.text().strip(),
            "username": self.user_page.line_input_username.text().strip(),
            "birth_date": self.user_page.cb_birth_date.dateTime().toString(
                "yyyy-MM-dd HH:mm:ss"
            ),
            "gender": self.user_page.cb_sex.currentText(),
            "phone": self.user_page.line_input_phone.text().strip(),
            "role": self.user_page.cb_role.currentText(),
            "is_active": 1 if self.user_page.cb_status.currentText() == "Activo" else 0,
            "email": self.user_page.line_input_email.text().strip(),
            "address": self.user_page.line_input_address.text().strip(),
        }

        if not self.validate_form_fields(user_data):
            return

        result = self.user_controller.update_user(user_data["user_id"], user_data)

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
            "phone": "Teléfono",
            "role": "Rol",
            "email": "Correo electrónico",
            "address": "Dirección",
            "is_active": "Estatus",
        }

        for key, value in user_data.items():
            if key == "is_active":
                if value not in [0, 1]:
                    QMessageBox.warning(
                        self.user_page,
                        "Error",
                        "El campo 'Estatus' debe ser 'Activo' o 'Inactivo'.",
                    )
                    return False
                continue

            if not value:
                field_name = translations.get(key, key)
                QMessageBox.warning(
                    self.user_page,
                    "Error",
                    f"El campo '{field_name}' no puede estar vacío.",
                )
                return False

        if not user_data["phone"].isdigit() or len(user_data["phone"]) != 10:
            QMessageBox.warning(
                self.user_page,
                "Error",
                "El número de teléfono debe contener exactamente 10 dígitos.",
            )
            return False

        return True
