from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox


class Main:
    def __init__(self):
        self.main = uic.loadUi("src/views/main_view.ui")
        self.main.show()

        self.main.icon_bar.setHidden(True)

        #seleccionar una pagina
        self.main.btn_users.clicked.connect(self.page_users)
        self.main.btn_users_2.clicked.connect(self.page_users)

        self.main.btn_products.clicked.connect(self.page_products)
        self.main.btn_products_2.clicked.connect(self.page_products)

        self.main.btn_machine.clicked.connect(self.page_machine)
        self.main.btn_machine_2.clicked.connect(self.page_machine)
        
        self.main.btn_boss.clicked.connect(self.page_boss)
        self.main.btn_boss_2.clicked.connect(self.page_boss)

    def page_users(self):
        self.main.stackedWidget.setCurrentIndex(0)

    def page_products(self):
        self.main.stackedWidget.setCurrentIndex(1)
    
    def page_machine(self):
        self.main.stackedWidget.setCurrentIndex(2)
    
    def page_boss(self):
        self.main.stackedWidget.setCurrentIndex(3)

