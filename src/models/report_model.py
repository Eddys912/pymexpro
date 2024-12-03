from src.database.connection import DBConnection


class ProductionReportModel:
    def __init__(
        self,
        manager_id=0,
        product_id=0,
        machine_id=0,
        produced_quantity=0,
        defective_quantity=0,
        production_date="",
        comments="",
    ):
        self._manager_id = manager_id
        self._product_id = product_id
        self._machine_id = machine_id
        self._produced_quantity = produced_quantity
        self._defective_quantity = defective_quantity
        self._production_date = production_date
        self._comments = comments
        self.db_connection = DBConnection()

    def _execute_query(self, query, params=None, fetch_one=False):
        try:
            conn = self.db_connection.connection()
            cursor = conn.cursor()
            cursor.execute(query, params)
            result = cursor.fetchone() if fetch_one else cursor.fetchall()
            conn.commit()
            return result
        except Exception as e:
            print(f"Error al ejecutar la consulta: {e}")
            return None
        finally:
            cursor.close()
            self.db_connection.close()

    def get_all_reports(self):
        query = "SELECT * FROM production_reports"
        return self._execute_query(query)

    def get_report_by_id(self, report_id):
        query = "SELECT * FROM production_reports WHERE report_id = %s"
        return self._execute_query(query, (report_id,), fetch_one=True)

    def create_report(self):
        query = """
            INSERT INTO production_reports (
                manager_id, product_id, machine_id, produced_quantity, defective_quantity, production_date, comments
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            self._manager_id,
            self._product_id,
            self._machine_id,
            self._produced_quantity,
            self._defective_quantity,
            self._production_date,
            self._comments,
        )
        result = self._execute_query(query, values)
        if result is None:
            return {"message": "Error al crear reporte de producción"}
        return {"message": "Reporte de producción creado correctamente"}

    def update_report(self, report_id):
        query = """
            UPDATE production_reports
            SET manager_id=%s, product_id=%s, machine_id=%s, produced_quantity=%s, defective_quantity=%s, 
                production_date=%s, comments=%s
            WHERE report_id=%s
        """
        values = (
            self._manager_id,
            self._product_id,
            self._machine_id,
            self._produced_quantity,
            self._defective_quantity,
            self._production_date,
            self._comments,
            report_id,
        )
        result = self._execute_query(query, values)
        if result is None:
            return {"message": "Error al actualizar reporte de producción"}
        return {"message": "Reporte de producción actualizado correctamente"}

    def delete_report(self, report_id):
        query = "DELETE FROM production_reports WHERE report_id = %s"
        result = self._execute_query(query, (report_id,))
        if result is None:
            return {"message": "Error al eliminar reporte de producción"}
        return {"message": "Reporte de producción eliminado correctamente"}
