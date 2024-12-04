from PyQt6.QtWidgets import QMessageBox
from src.controllers.user_controller import UserController
from src.utils.base_page import BasePage
from src.views.buttons_actions import ButtonsAction
from src.views.forms.form_create_user import FormCreateUser
from src.views.forms.form_update_user import FormUpdateUser


class PageUsers(BasePage):
    COLUMN_WIDTHS = [120, 100, 80, 150, 80, 10, 80, 120, 40]
    COLUMN_KEYS = [
        "full_name",
        "role",
        "username",
        "email",
        "formatted_phone",
        "age",
        "gender",
        "address",
        "is_active_status",
    ]

    def __init__(self, main, table_widget):
        BasePage.__init__(self, main, table_widget)
        self.user_controller = UserController()
        self.column_keys = self.COLUMN_KEYS
        self.row_widget_creator = self.create_row_buttons

    def setup_ui(self):
        self.setup_table(self.COLUMN_WIDTHS)

        # Configurar filtros si los combobox existen
        if hasattr(self.main, "cb_filter_role") and hasattr(self.main, "cb_filter_sex"):
            self.setup_filters(
                {"role": self.main.cb_filter_role, "gender": self.main.cb_filter_sex}
            )

        # Configurar búsqueda si el campo existe
        if hasattr(self.main, "line_search_user"):
            self.setup_search(self.main.line_search_user)

    def load_users(self):
        try:
            self.load_data(
                self.user_controller.get_all_users,
                self.column_keys,
                self.row_widget_creator,
            )
        except Exception as e:
            QMessageBox.critical(
                self.main,
                "Error",
                f"Se produjo un error al cargar los usuarios: {str(e)}",
            )

    def form_create_user(self):
        self.form_create = FormCreateUser(self.main, self.load_users)

    def form_update_user(self, user_data):
        from PyQt6.QtCore import QDateTime

        self.form_update = FormUpdateUser(self, user_data)
        if isinstance(user_data["birth_date"], str):
            user_data["birth_date"] = QDateTime.fromString(
                user_data["birth_date"], "yyyy-MM-dd HH:mm:ss"
            )
        self.form_update.set_values(user_data)

    def delete_user(self, user_data):
        confirm = QMessageBox.question(
            self.main,
            "Eliminar usuario",
            f"Seguro que quiere eliminar el usuario {user_data['username']}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if confirm == QMessageBox.StandardButton.Yes:
            result = self.user_controller.delete_user(user_data["user_id"])
            if result["success"]:
                QMessageBox.information(self.main, "Éxito", result["message"])
                self.load_users()
            else:
                QMessageBox.warning(self.main, "Error", result["message"])

    def create_row_buttons(self, row_index, row_data):
        return ButtonsAction(
            row_index,
            row_data,
            self,
            edit_method="form_update_user",
            delete_method="delete_user",
        )

    def fetch_filtered_data(self, filter_values, search_text):
        role = filter_values.get("role", "Seleccionar rol")
        gender = filter_values.get("gender", "Seleccionar sexo")

        if (
            role == "Seleccionar rol"
            and gender == "Seleccionar sexo"
            and not search_text
        ):
            return self.user_controller.get_all_users()
        elif search_text:
            return self.user_controller.get_search_users(search_text)
        else:
            return self.user_controller.get_filtered_users(role, gender)
