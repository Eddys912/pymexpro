from src.models.report_model import ProductionReportModel


class ProductionReportController:
    def get_all_reports(self):
        try:
            report_model = ProductionReportModel()
            reports = report_model.get_all_reports()
            return (
                reports
                if reports
                else {"message": "No se encontraron reportes de producción."}
            )
        except Exception as e:
            print(f"Error al obtener reportes: {e}")
            return {"message": "Error al obtener reportes."}

    def create_report(
        self,
        manager_id,
        product_id,
        machine_id,
        produced_quantity,
        defective_quantity,
        production_date,
        comments,
    ):
        try:
            if not all(
                [manager_id, product_id, machine_id, produced_quantity, production_date]
            ):
                return {
                    "message": "Todos los campos obligatorios no pueden estar vacíos."
                }
            new_report = ProductionReportModel(
                manager_id=manager_id,
                product_id=product_id,
                machine_id=machine_id,
                produced_quantity=produced_quantity,
                defective_quantity=defective_quantity,
                production_date=production_date,
                comments=comments,
            )
            return new_report.create_report()
        except Exception as e:
            print(f"Error al crear reporte de producción: {e}")
            return {"message": "Error al crear reporte de producción."}

    def update_report(self, report_id, **kwargs):
        try:
            report_model = ProductionReportModel()
            existing_report = report_model.get_report_by_id(report_id)
            if not existing_report:
                return {"message": "El reporte no existe."}

            updated_report = ProductionReportModel(
                manager_id=kwargs.get("manager_id", existing_report[1]),
                product_id=kwargs.get("product_id", existing_report[2]),
                machine_id=kwargs.get("machine_id", existing_report[3]),
                produced_quantity=kwargs.get("produced_quantity", existing_report[4]),
                defective_quantity=kwargs.get("defective_quantity", existing_report[5]),
                production_date=kwargs.get("production_date", existing_report[6]),
                comments=kwargs.get("comments", existing_report[7]),
            )
            return updated_report.update_report(report_id)
        except Exception as e:
            print(f"Error al actualizar reporte con ID {report_id}: {e}")
            return {"message": "Error al actualizar reporte de producción."}

    def delete_report(self, report_id):
        try:
            report_model = ProductionReportModel()
            existing_report = report_model.get_report_by_id(report_id)
            if not existing_report:
                return {"message": "El reporte no existe."}
            return report_model.delete_report(report_id)
        except Exception as e:
            print(f"Error al eliminar reporte con ID {report_id}: {e}")
            return {"message": "Error al eliminar reporte de producción."}
