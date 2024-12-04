import os
from PyQt6 import uic
from src.utils.export_excel import ExportExcel
from src.utils.export_pdf import ExportPDF
from src.views.page_machines import PageMachines
from src.views.page_users import PageUsers


class Main:
    def __init__(self):
        self.main = uic.loadUi("src/views/main_view.ui")
        self.main.show()
        self.setup_ui()

    def setup_ui(self):
        self.setup_pages()
        self.setup_buttons()
        self.main.icon_bar.setHidden(True)

    def setup_pages(self):
        self.page_user = PageUsers(self.main, self.main.table_users)
        self.page_user.setup_ui()

        self.page_machine = PageMachines(self.main, self.main.table_machines)
        self.page_machine.setup_ui()

    def setup_buttons(self):
        self.export_pdf = ExportPDF(
            self.main.table_users, self.main, "Reporte de Usuarios"
        )
        self.export_excel = ExportExcel(
            self.main.table_users, self.main, "Reporte de Usuarios"
        )
        self.export_pdf_2 = ExportPDF(
            self.main.table_machines, self.main, "Reporte de Máquinas"
        )
        self.export_excel_2 = ExportExcel(
            self.main.table_machines, self.main, "Reporte de Máquinas"
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
        self.main.btn_add_user.clicked.connect(self.page_user.form_create_user)
        self.main.btn_add_machine.clicked.connect(self.page_machine.form_create_machine)
        self.main.btn_export_excel.clicked.connect(self.export_excel.export_to_excel)
        self.main.btn_export_pdf.clicked.connect(self.export_pdf.export_to_pdf)
        self.main.btn_export_excel_2.clicked.connect(self.export_excel_2.export_to_excel)
        self.main.btn_export_pdf_2.clicked.connect(self.export_pdf_2.export_to_pdf)

        self.main.btn_add_user.clicked.connect(self.page_user.load_users)
        self.main.btn_add_machine.clicked.connect(self.page_machine.load_machines)

    def connect_buttons(self, button_groups):
        for buttons in button_groups:
            action = buttons[-1]
            for btn in buttons[:-1]:
                btn.clicked.connect(action)

    def navigate_to_users(self):
        self.main.stackedWidget.setCurrentIndex(0)
        self.page_user.load_users()

    def navigate_to_products(self):
        self.main.stackedWidget.setCurrentIndex(1)

    def navigate_to_machine(self):
        self.main.stackedWidget.setCurrentIndex(2)
        self.page_machine.load_machines()

    def navigate_to_boss(self):
        self.main.stackedWidget.setCurrentIndex(3)

    def logout(self):
        from src.views.login import Login

        self.main.close()
        self.login = Login()
