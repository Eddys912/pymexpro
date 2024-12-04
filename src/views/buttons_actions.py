import os
from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QPushButton,
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize


class ButtonsAction(QWidget):
    def __init__(self, row_index, row_data, parent, edit_method, delete_method):
        super().__init__()
        self.row_index = row_index
        self.row_data = row_data
        self.parent = parent
        self.edit_method = edit_method
        self.delete_method = delete_method
        self.setup_ui()

    def setup_ui(self):
        self.layout = QHBoxLayout(self)
        self.icons_path = self.get_icons_path()
        self.btn_edit = self.create_button("edit.png", "#FFC107", (30, 30))
        self.btn_delete = self.create_button("delete.png", "#F44336", (30, 30))

        self.btn_edit.clicked.connect(
            lambda: getattr(self.parent, self.edit_method)(self.row_data)
        )
        self.btn_delete.clicked.connect(
            lambda: getattr(self.parent, self.delete_method)(self.row_data)
        )

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
