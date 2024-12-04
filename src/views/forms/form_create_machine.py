from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox
from src.controllers.machine_controller import MachineController


class FormCreateMachine:
    def __init__(self, main_window, on_machine_created):
        self.machine_page = uic.loadUi("src/views/forms/form_create_machine.ui")
        self.machine_page.show()
        self.machine_controller = MachineController()
        self.main_window = main_window
        self.on_machine_created = on_machine_created
        self.machine_page.btn_create_machine.clicked.connect(self.form_create_machine)

    def form_create_machine(self):

        machine_data = {
            "machine_name": self.machine_page.line_input_machine_name.text().strip(),
            "type": self.machine_page.cb_type.currentText(),
            "production_capacity": self.machine_page.line_input_capacity.text().strip(),
            "status": self.machine_page.cb_status.currentText(),
            "installation_date": self.machine_page.cb_date_installation.date().toString(
                "yyyy-MM-dd"
            ),
            "last_maintenance": self.machine_page.cb_date_last_maintenance.date().toString(
                "yyyy-MM-dd"
            ),
            "responsible": self.machine_page.line_input_responsible.text().strip(),
        }

        if not self.validate_form_fields(machine_data):
            return

        result = self.machine_controller.create_machine(machine_data)

        if result["success"]:
            QMessageBox.information(self.machine_page, "Éxito", result["message"])
            if self.on_machine_created:
                self.on_machine_created()
            self.machine_page.close()
        else:
            QMessageBox.warning(self.machine_page, "Error", result["message"])

    def validate_form_fields(self, machine_data):
        translations = {
            "machine_name": "Nombre de la máquina",
            "type": "Tipo",
            "production_capacity": "Capacidad de producción",
            "status": "Estado",
            "installation_date": "Fecha de instalación",
            "last_maintenance": "Último mantenimiento",
            "responsible": "Responsable",
        }

        for key, value in machine_data.items():
            if not value and key not in ["last_maintenance", "production_capacity"]:
                field_name = translations.get(key, key)
                QMessageBox.warning(
                    self.machine_page,
                    "Error",
                    f"El campo '{field_name}' no puede estar vacío.",
                )
                return False

        if machine_data["type"] == "Seleccionar tipo":
            QMessageBox.warning(
                self.machine_page, "Error", "Debe seleccionar un tipo válido."
            )
            return False

        if machine_data["status"] not in ["Operativa", "Mantenimiento"]:
            QMessageBox.warning(
                self.machine_page, "Error", "Debe seleccionar un estado válido."
            )
            return False

        if (
            machine_data["production_capacity"]
            and not machine_data["production_capacity"].isdigit()
        ):
            QMessageBox.warning(
                self.machine_page,
                "Error",
                "La capacidad de producción debe ser un número entero.",
            )
            return False

        return True
