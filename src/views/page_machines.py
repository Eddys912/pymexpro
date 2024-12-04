from PyQt6.QtWidgets import QMessageBox
from src.controllers.machine_controller import MachineController
from src.utils.base_page import BasePage
from src.views.buttons_actions import ButtonsAction
from src.views.forms.form_create_machine import FormCreateMachine
from src.views.forms.form_update_machine import FormUpdateMachine


class PageMachines(BasePage):
    COLUMN_WIDTHS = [120, 100, 80, 150, 100, 90, 90, 50]
    COLUMN_KEYS = [
        "machine_name",
        "type",
        "production_capacity",
        "responsible",
        "status",
        "installation_date",
        "last_maintenance",
        "is_active_status",
    ]

    def __init__(self, main, table_widget):
        super().__init__(main, table_widget)
        self.machine_controller = MachineController()
        self.column_keys = self.COLUMN_KEYS
        self.row_widget_creator = self.create_row_buttons

    def setup_ui(self):
        self.setup_table(self.COLUMN_WIDTHS)

        # Configurar filtros si los combobox existen
        if hasattr(self.main, "cb_filter_status") and hasattr(
            self.main, "cb_filter_type"
        ):
            self.setup_filters(
                {"status": self.main.cb_filter_status, "type": self.main.cb_filter_type}
            )

        # Configurar búsqueda si el campo existe
        if hasattr(self.main, "line_search_machine"):
            self.setup_search(self.main.line_search_machine)

    def load_machines(self):
        try:
            self.load_data(
                self.machine_controller.get_all_machines,
                self.column_keys,
                self.row_widget_creator,
            )
        except Exception as e:
            QMessageBox.critical(
                self.main,
                "Error",
                f"Se produjo un error al cargar las máquinas: {str(e)}",
            )

    def form_create_machine(self):
        self.form_create = FormCreateMachine(self.main, self.load_machines)

    def form_update_machine(self, machine_data):
        self.form_update = FormUpdateMachine(self, machine_data)
        self.form_update.set_values(machine_data)

    def delete_machine(self, machine_data):
        confirm = QMessageBox.question(
            self.main,
            "Eliminar máquina",
            f"Seguro que quiere eliminar la máquina {machine_data['machine_name']}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if confirm == QMessageBox.StandardButton.Yes:
            result = self.machine_controller.delete_machine(machine_data["machine_id"])
            if result["success"]:
                QMessageBox.information(self.main, "Éxito", result["message"])
                self.load_machines()
            else:
                QMessageBox.warning(self.main, "Error", result["message"])

    def create_row_buttons(self, row_index, row_data):
        return ButtonsAction(
            row_index,
            row_data,
            self,
            edit_method="form_update_machine",
            delete_method="delete_machine",
        )

    def fetch_filtered_data(self, filter_values, search_text):
        status = filter_values.get("status", "Seleccionar estatus")
        machine_type = filter_values.get("type", "Seleccionar tipo")

        if (
            status == "Seleccionar estatus"
            and machine_type == "Seleccionar tipo"
            and not search_text
        ):
            return self.machine_controller.get_all_machines()
        elif search_text:
            return self.machine_controller.get_search_machines(search_text)
        else:
            return self.machine_controller.get_filtered_machines(status, machine_type)
