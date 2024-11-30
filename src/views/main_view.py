from PyQt6 import uic
from PyQt6.QtWidgets import QTableWidgetItem, QWidget, QHBoxLayout, QPushButton
from PyQt6.QtGui import QIcon
from src.views.create_user import UserPage
from src.controllers.user_controller import UserController

COLUMN_WIDTHS = [90, 160, 80, 80, 120, 100, 120, 50, 110]


class Main:
    def __init__(self):
        self.main = uic.loadUi("src/views/main_view.ui")
        self.main.show()
        self.init()
        self.init_table()
        self.view_users()
        self.main.icon_bar.setHidden(True)

    def init(self):
        self.main.btn_add_student.clicked.connect(self.user_form)
        self.connect_buttons(
            [
                (self.main.btn_users, self.main.btn_users_2, self.page_users),
                (self.main.btn_products, self.main.btn_products_2, self.page_products),
                (self.main.btn_machine, self.main.btn_machine_2, self.page_machine),
                (self.main.btn_boss, self.main.btn_boss_2, self.page_boss),
            ]
        )

    def connect_buttons(self, button_groups):
        for buttons in button_groups:
            action = buttons[-1]
            for btn in buttons[:-1]:
                btn.clicked.connect(action)

    def init_table(self):
        self.set_table_column_widths(self.main.table_users, COLUMN_WIDTHS)

    def set_table_column_widths(self, table, widths):
        for index, width in enumerate(widths):
            table.setColumnWidth(index, width)

    def user_form(self):
        self.main = UserPage()

    def page_users(self):
        self.main.stackedWidget.setCurrentIndex(0)

    def page_products(self):
        self.main.stackedWidget.setCurrentIndex(1)

    def page_machine(self):
        self.main.stackedWidget.setCurrentIndex(2)

    def page_boss(self):
        self.main.stackedWidget.setCurrentIndex(3)

    def view_users(self):
        self.populate_table(self.main.table_users, UserController().get_all_users())

    def populate_table(self, table, data):
        table.setRowCount(0)
        for row_index, row_data in enumerate(data):
            table.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                table.setItem(row_index, col_index, QTableWidgetItem(str(cell_data)))
            table.setCellWidget(
                row_index, 8, DoubleButtonWidgetsStudents(row_index, row_data)
            )
            table.setRowHeight(row_index, 50)


import os
from PyQt6.QtCore import QSize


class DoubleButtonWidgetsStudents(QWidget):
    def __init__(self, row_index, row_data):
        super().__init__()
        self.row_index = row_index
        self.row_data = row_data

        # Calcula la ruta al directorio de íconos
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
        icons_path = os.path.join(base_dir, "public", "icons")

        self.layout = QHBoxLayout(self)
        self.btn_edit = self.create_button(
            os.path.join(icons_path, "edit.png"), "#FFC107", (30, 30)
        )
        self.btn_delete = self.create_button(
            os.path.join(icons_path, "delete.png"), "#F44336", (30, 30)
        )

        self.layout.addWidget(self.btn_edit)
        self.layout.addWidget(self.btn_delete)

    def create_button(self, icon_path, color, size):
        if not os.path.exists(icon_path):
            print(f"Error: El icono no existe en {icon_path}")
            return QPushButton("", self)

        btn = QPushButton("", self)
        btn.setStyleSheet(f"background-color: {color}")
        btn.setFixedSize(*size)

        # Cargar el icono desde el archivo
        icon = QIcon(icon_path)
        btn.setIcon(icon)
        size_btn = 25, 25
        btn.setIconSize(QSize(*size_btn))
        return btn
