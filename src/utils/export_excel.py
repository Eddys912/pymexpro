from PyQt6.QtWidgets import QMessageBox, QFileDialog
import pandas as pd
from datetime import datetime


class ExportExcel:
    def __init__(self, table_widget, parent, title="Reporte de Datos"):
        self.table_widget = table_widget
        self.parent = parent
        self.title = title

    def get_table_data(self):
        data = []
        row_count = self.table_widget.rowCount()
        column_count = self.table_widget.columnCount() - 1  # Excluye la última columna

        for row in range(row_count):
            row_data = {}
            for col in range(column_count):
                header = self.table_widget.horizontalHeaderItem(col).text()
                item = self.table_widget.item(row, col)
                row_data[header] = item.text() if item else ""
            data.append(row_data)

        return data

    def export_to_excel(self):
        data = self.get_table_data()
        if not data:
            QMessageBox.warning(
                self.parent, "Advertencia", "No hay datos para exportar."
            )
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self.parent, "Guardar como", "", "Archivos Excel (*.xlsx)"
        )
        if not file_path:
            return

        try:
            df = pd.DataFrame(data)
            metadata = {
                "Nombre del Reporte": self.title,
                "Generado por": "Usuario Actual",
                "Fecha de Generación": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Total de Columnas": len(df.columns),
                "Total de Filas": len(df),
            }

            with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
                df.to_excel(writer, index=False, sheet_name="Datos")
                meta_df = pd.DataFrame(
                    metadata.items(), columns=["Información", "Valor"]
                )
                meta_df.to_excel(writer, index=False, sheet_name="Metadatos")

            QMessageBox.information(
                self.parent, "Éxito", "Archivo Excel exportado correctamente."
            )
        except Exception as e:
            QMessageBox.critical(self.parent, "Error", f"Error al exportar Excel: {e}")
