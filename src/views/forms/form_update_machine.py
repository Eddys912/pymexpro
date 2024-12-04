from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox
from src.controllers.machine_controller import MachineController


class FormUpdateMachine:
    def __init__(self, main_window, machine_data):
        self.machine_page = uic.loadUi("src/views/forms/form_update_machine.ui")
        self.machine_page.show()
        self.machine_controller = MachineController()
        self.main_window = main_window
        self.machine_data = machine_data

        self.machine_page.btn_update_machine.clicked.connect(self.form_update_machine)
        self.set_values(machine_data)

    def set_values(self, machine_data):
        self.machine_page.line_input_machine_name.setText(machine_data["machine_name"])
        self.machine_page.cb_type.setCurrentText(machine_data["type"])
        self.machine_page.line_input_capacity.setText(str(machine_data["production_capacity"]))
        self.machine_page.cb_status.setCurrentText(machine_data["status"])
        self.machine_page.cb_date_installation.setDate(machine_data["installation_date"])
        self.machine_page.cb_date_last_maintenance.setDate(machine_data["last_maintenance"])
        self.machine_page.line_input_responsible.setText(machine_data["responsible"])

        is_active_text = "Activa" if machine_data["is_active"] == 1 else "Inactiva"
        self.machine_page.cb_is_active.setCurrentText(is_active_text)

    def form_update_machine(self):
        machine_data = {
            "machine_id": self.machine_data["machine_id"],
            "machine_name": self.machine_page.line_input_machine_name.text().strip(),
            "type": self.machine_page.cb_type.currentText(),
            "production_capacity": self.machine_page.line_input_capacity.text().strip(),
            "status": self.machine_page.cb_status.currentText(),
            "installation_date": self.machine_page.cb_date_installation.date().toString("yyyy-MM-dd"),
            "last_maintenance": self.machine_page.cb_date_last_maintenance.date().toString("yyyy-MM-dd"),
            "responsible": self.machine_page.line_input_responsible.text().strip(),
            "is_active": 1 if self.machine_page.cb_is_active.currentText() == "Activa" else 0
        }

        if not self.validate_form_fields(machine_data):
            return

        result = self.machine_controller.update_machine(machine_data["machine_id"], machine_data)

        if result["success"]:
            QMessageBox.information(self.machine_page, "Éxito", result["message"])
            self.main_window.apply_filters()
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
            "is_active": "Activo",
        }

        for key, value in machine_data.items():
            if key in ["last_maintenance", "production_capacity"] and not value:
                continue  # Estos campos son opcionales

            if not value and key not in ["is_active"]:
                field_name = translations.get(key, key)
                QMessageBox.warning(
                    self.machine_page,
                    "Error",
                    f"El campo '{field_name}' no puede estar vacío.",
                )
                return False

            if key == "production_capacity" and value and not value.isdigit():
                QMessageBox.warning(
                    self.machine_page,
                    "Error",
                    "La capacidad de producción debe ser un número entero.",
                )
                return False

        if machine_data["status"] not in ["Operativa", "Mantenimiento"]:
            QMessageBox.warning(
                self.machine_page, "Error", "Debe seleccionar un estado válido."
            )
            return False

        return True
