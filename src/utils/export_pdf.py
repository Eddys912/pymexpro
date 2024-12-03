from fpdf import FPDF
from datetime import datetime
from PyQt6.QtWidgets import QMessageBox, QFileDialog


class ExportPDF:
    def __init__(self, table_widget, parent, title="Reporte"):
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

    def calculate_column_widths(self, data, pdf, headers, max_width):
        col_widths = []
        for i, header in enumerate(headers):
            max_content_width = (
                pdf.get_string_width(header) + 10
            )  # Ancho mínimo del encabezado
            for row in data:
                content_width = pdf.get_string_width(str(row[header])) + 10
                max_content_width = max(max_content_width, content_width)
            col_widths.append(
                min(max_width, max_content_width)
            )  # Limita el ancho máximo de columnas
        total_width = sum(col_widths)
        scaling_factor = (pdf.w - 2 * pdf.l_margin) / total_width
        return [
            int(w * scaling_factor) for w in col_widths
        ]  # Ajustar al ancho total disponible

    def export_to_pdf(self):
        data = self.get_table_data()
        if not data:
            QMessageBox.warning(
                self.parent, "Advertencia", "No hay datos para exportar."
            )
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self.parent, "Guardar como", "", "Archivos PDF (*.pdf)"
        )
        if not file_path:
            return

        try:
            pdf = FPDF(orientation="L", unit="mm", format="A4")
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()

            pdf.set_font("Arial", size=18)

            # Información de cabecera
            company_name = "PyMexPro"
            generated_by = "Generado por: Eduardo David Peña Araujo"
            generation_date = (
                f"Fecha de Generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )
            total_columns = f"Total de Columnas: {len(data[0].keys())}"

            pdf.set_font("Arial", "B", 14)
            pdf.cell(0, 10, company_name, ln=True, align="C")
            pdf.ln(5)

            pdf.set_font("Arial", size=10)
            pdf.cell(0, 8, generated_by, ln=True, align="L")
            pdf.cell(0, 8, generation_date, ln=True, align="L")
            pdf.cell(0, 8, total_columns, ln=True, align="L")
            pdf.ln(10)

            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 10, self.title, ln=True, align="C")
            pdf.ln(5)

            # Configuración de las columnas
            headers = list(data[0].keys())
            col_widths = self.calculate_column_widths(data, pdf, headers, max_width=50)

            # Dibujar encabezados
            pdf.set_font("Arial", "B", 9)
            for i, header in enumerate(headers):
                pdf.cell(col_widths[i], 8, header, border=1, align="C")
            pdf.ln()

            # Dibujar filas de la tabla
            pdf.set_font("Arial", size=8)
            for row in data:
                max_height = 8
                for i, header in enumerate(headers):
                    x = pdf.get_x()
                    y = pdf.get_y()
                    pdf.multi_cell(
                        col_widths[i], 6, str(row[header]), border=1, align="L"
                    )
                    max_height = max(max_height, pdf.get_y() - y)
                    pdf.set_xy(x + col_widths[i], y)
                pdf.ln(max_height)

            pdf.output(file_path)
            QMessageBox.information(
                self.parent, "Éxito", "Archivo PDF exportado correctamente."
            )
        except Exception as e:
            QMessageBox.critical(self.parent, "Error", f"Error al exportar PDF: {e}")
