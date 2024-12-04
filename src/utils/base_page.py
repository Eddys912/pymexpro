from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox


class BasePage:
    def __init__(self, main, table_widget):
        self.main = main
        self.table_widget = table_widget
        self.filters = {}
        self.search_line = None

    def setup_table(self, column_widths):
        for index, width in enumerate(column_widths):
            self.table_widget.setColumnWidth(index, width)

    def populate_table(self, data, column_keys, row_widget_creator=None):
        self.table_widget.setRowCount(0)
        for row_index, row_data in enumerate(data):
            self.table_widget.insertRow(row_index)
            for col_index, key in enumerate(column_keys):
                self.table_widget.setItem(
                    row_index, col_index, QTableWidgetItem(str(row_data[key]))
                )
            if row_widget_creator:
                buttons_widget = row_widget_creator(row_index, row_data)
                self.table_widget.setCellWidget(
                    row_index, len(column_keys), buttons_widget
                )
                self.table_widget.setRowHeight(row_index, 50)

    def clear_table(self):
        self.table_widget.setRowCount(0)

    def load_data(self, data_fetcher, column_keys, row_widget_creator=None):
        try:
            response = data_fetcher()  # Llama al controlador
            if not response.get("success", False):
                self.clear_table()
                QMessageBox.information(
                    self.main,
                    "Información",
                    response.get("message", "Error desconocido"),
                )
                return

            # Verifica que los datos sean una lista
            data = response.get("data", [])
            if not isinstance(data, list):
                raise ValueError(
                    "El formato de los datos no es válido. Se esperaba una lista."
                )

            self.populate_table(data, column_keys, row_widget_creator)
        except Exception as e:
            QMessageBox.critical(
                self.main, "Error", f"Se produjo un error al cargar los datos: {str(e)}"
            )
            self.clear_table()

    def setup_filters(self, filter_comboboxes):
        self.filters = filter_comboboxes
        for combobox in self.filters.values():
            combobox.currentIndexChanged.connect(self.apply_filters)

    def setup_search(self, search_line):
        self.search_line = search_line
        self.search_line.textChanged.connect(self.apply_filters)

    def apply_filters(self):
        try:
            filter_values = {key: cb.currentText() for key, cb in self.filters.items()}
            search_text = self.search_line.text() if self.search_line else None

            # Asegura que las claves estén definidas
            column_keys = getattr(self, "column_keys", None)
            row_widget_creator = getattr(self, "row_widget_creator", None)

            if not column_keys:
                raise AttributeError("No se definió column_keys en la subclase.")
            if not row_widget_creator:
                raise AttributeError("No se definió row_widget_creator en la subclase.")

            data = self.fetch_filtered_data(filter_values, search_text)
            if not data.get("success", False):
                self.clear_table()
                QMessageBox.information(
                    self.main, "Información", data.get("message", "Error desconocido")
                )
                return

            self.populate_table(data.get("data", []), column_keys, row_widget_creator)
        except Exception as e:
            QMessageBox.critical(
                self.main,
                "Error",
                f"Se produjo un error al aplicar los filtros: {str(e)}",
            )

    def fetch_filtered_data(self, filter_values, search_text):
        """
        Método abstracto para ser sobrescrito en cada página.
        """
        raise NotImplementedError(
            "fetch_filtered_data debe ser implementado por la subclase"
        )
