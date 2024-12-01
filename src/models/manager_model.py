from src.database.connection import DBConnection

class ManagerModel:
    def __init__(self, manager_id=0, shift="", responsible_area="", registration_date=""):
        self._manager_id = manager_id
        self._shift = shift
        self._responsible_area = responsible_area
        self._registration_date = registration_date
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

    def get_all_managers(self):
        query = "SELECT * FROM managers"
        return self._execute_query(query)

    def get_manager_by_id(self, manager_id):
        query = "SELECT * FROM managers WHERE manager_id = %s"
        return self._execute_query(query, (manager_id,), fetch_one=True)

    def create_manager(self):
        query = """
            INSERT INTO managers (manager_id, shift, responsible_area, registration_date)
            VALUES (%s, %s, %s, %s)
        """
        values = (
            self._manager_id,
            self._shift,
            self._responsible_area,
            self._registration_date,
        )
        result = self._execute_query(query, values)
        if result is None:
            return {"message": "Error al crear gerente"}
        return {"message": "Gerente creado correctamente"}

    def update_manager(self, manager_id):
        query = """
            UPDATE managers
            SET shift=%s, responsible_area=%s, registration_date=%s
            WHERE manager_id=%s
        """
        values = (
            self._shift,
            self._responsible_area,
            self._registration_date,
            manager_id,
        )
        result = self._execute_query(query, values)
        if result is None:
            return {"message": "Error al actualizar gerente"}
        return {"message": "Gerente actualizado correctamente"}

    def delete_manager(self, manager_id):
        query = "DELETE FROM managers WHERE manager_id = %s"
        result = self._execute_query(query, (manager_id,))
        if result is None:
            return {"message": "Error al eliminar gerente"}
        return {"message": "Gerente eliminado correctamente"}
