import os
from PyQt6 import uic
from PyQt6.QtWidgets import (
    QTableWidgetItem,
    QWidget,
    QHBoxLayout,
    QPushButton,
    QMessageBox,
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize
from src.controllers.user_controller import UserController
from src.views.form_create_user import FormCreate
from src.views.form_update_user import FormUpdate
from src.utils.export_excel import ExportExcel
from src.utils.export_pdf import ExportPDF

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


class Main:
    def __init__(self):
        self.main = uic.loadUi("src/views/main_view.ui")
        self.main.show()
        self.setup_ui()

    def setup_ui(self):
        self.setup_buttons()
        self.setup_table()
        self.setup_filters()
        self.setup_search()
        self.load_users(UserController().get_all_users())
        self.main.icon_bar.setHidden(True)

    def setup_buttons(self):
        self.export_pdf = ExportPDF(
            self.main.table_users, self.main, "Reporte de Usuarios"
        )
        self.export_excel = ExportExcel(
            self.main.table_users, self.main, "Reporte de Usuarios"
        )
        button_groups = [
            (self.main.btn_users, self.main.btn_users_2, self.navigate_to_users),
            (
                self.main.btn_products,
                self.main.btn_products_2,
                self.navigate_to_products,
            ),
            (self.main.btn_machine, self.main.btn_machine_2, self.navigate_to_machine),
            (self.main.btn_boss, self.main.btn_boss_2, self.navigate_to_boss),
            (self.main.btn_logout, self.main.btn_logout_2, self.logout),
        ]
        self.connect_buttons(button_groups)
        self.main.btn_add_student.clicked.connect(self.form_create_user)
        self.main.btn_export_excel.clicked.connect(self.export_excel.export_to_excel)
        self.main.btn_export_pdf.clicked.connect(self.export_pdf.export_to_pdf)

    def connect_buttons(self, button_groups):
        for buttons in button_groups:
            action = buttons[-1]
            for btn in buttons[:-1]:
                btn.clicked.connect(action)

    def setup_table(self):
        for index, width in enumerate(COLUMN_WIDTHS):
            self.main.table_users.setColumnWidth(index, width)

    def setup_filters(self):
        self.main.cb_filter_role.currentIndexChanged.connect(self.apply_filters)
        self.main.cb_filter_sex.currentIndexChanged.connect(self.apply_filters)

    def setup_search(self):
        self.main.line_search_user.textChanged.connect(self.apply_filters)

    def apply_filters(self):
        role = self.main.cb_filter_role.currentText()
        gender = self.main.cb_filter_sex.currentText()
        search_text = self.main.line_search_user.text()

        if (
            role == "Seleccionar rol"
            and gender == "Seleccionar sexo"
            and not search_text
        ):
            users = UserController().get_all_users()
        elif search_text:
            users = UserController().get_search_users(search_text)
        else:
            users = UserController().get_filtered_users(role, gender)

        if not users["success"]:
            self.clear_table()
            QMessageBox.information(self.main, "Usuarios", users["message"])
        else:
            self.populate_table(users["data"])

    def load_users(self, users):
        if not users["success"]:
            self.clear_table()
            QMessageBox.information(self.main, "Usuarios", users["message"])
        else:
            self.populate_table(users["data"])

    def populate_table(self, data):
        self.main.table_users.setRowCount(0)
        for row_index, row_data in enumerate(data):
            self.main.table_users.insertRow(row_index)
            for col_index, key in enumerate(COLUMN_KEYS):
                self.main.table_users.setItem(
                    row_index, col_index, QTableWidgetItem(str(row_data[key]))
                )
            buttons_widget = DoubleButtonWidgetsStudents(
                row_index=row_index, row_data=row_data, parent=self
            )
            self.main.table_users.setCellWidget(
                row_index, len(COLUMN_KEYS), buttons_widget
            )
            self.main.table_users.setRowHeight(row_index, 50)

    def clear_table(self):
        self.main.table_users.setRowCount(0)

    def navigate_to_users(self):
        self.main.stackedWidget.setCurrentIndex(0)

    def navigate_to_products(self):
        self.main.stackedWidget.setCurrentIndex(1)

    def navigate_to_machine(self):
        self.main.stackedWidget.setCurrentIndex(2)

    def navigate_to_boss(self):
        self.main.stackedWidget.setCurrentIndex(3)

    def form_create_user(self):
        self.user_page = FormCreate(self)

    def form_update_user(self, user_data):
        from PyQt6.QtCore import QDateTime

        self.form_update = FormUpdate(self, user_data)

        if isinstance(user_data["birth_date"], str):
            user_data["birth_date"] = QDateTime.fromString(
                user_data["birth_date"], "yyyy-MM-dd HH:mm:ss"
            )

        self.form_update.set_values(user_data)

    def delete_user(self, user_data):
        confirm = QMessageBox.question(
            self.main,
            "Eliminar Usuario",
            f"¿Seguro que quiere eliminar el usuario {user_data['username']}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if confirm == QMessageBox.StandardButton.Yes:
            result = UserController().delete_user(user_data["user_id"])
            if result["success"]:
                QMessageBox.information(self.main, "Éxito", result["message"])
                self.apply_filters()
            else:
                QMessageBox.warning(self.main, "Error", result["message"])

    def logout(self):
        from src.views.login import Login

        self.main.close()
        self.login = Login()


class DoubleButtonWidgetsStudents(QWidget):
    def __init__(self, row_index, row_data, parent):
        super().__init__()
        self.row_index = row_index
        self.row_data = row_data
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        self.layout = QHBoxLayout(self)
        self.icons_path = self.get_icons_path()
        self.btn_edit = self.create_button("edit.png", "#FFC107", (30, 30))
        self.btn_delete = self.create_button("delete.png", "#F44336", (30, 30))

        self.btn_edit.clicked.connect(
            lambda: self.parent.form_update_user(self.row_data)
        )
        self.btn_delete.clicked.connect(lambda: self.parent.delete_user(self.row_data))

        self.layout.addWidget(self.btn_edit)
        self.layout.addWidget(self.btn_delete)

    def get_icons_path(self):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
        icons_path = os.path.join(base_dir, "public", "icons")
        if not os.path.exists(icons_path):
            raise FileNotFoundError(f"El directorio de íconos no existe: {icons_path}")
        return icons_path

    def create_button(self, icon_name, color, size):
        icon_path = os.path.join(self.icons_path, icon_name)
        if not os.path.exists(icon_path):
            raise FileNotFoundError(f"El ícono no existe en {icon_path}")
        btn = QPushButton("", self)
        btn.setStyleSheet(f"background-color: {color}")
        btn.setFixedSize(*size)
        btn.setIcon(QIcon(icon_path))
        btn.setIconSize(QSize(25, 25))
        return btn
