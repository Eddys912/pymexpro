from src.database.connection import DBConnection


class MachineModel:
    def __init__(
        self,
        machine_name="",
        type="",
        production_capacity=0,
        status="Operativa",
        installation_date="",
        last_maintenance="",
        responsible="",
        is_active=True,
    ):
        self._machine_name = machine_name
        self._type = type
        self._production_capacity = production_capacity
        self._status = status
        self._installation_date = installation_date
        self._last_maintenance = last_maintenance
        self._responsible = responsible
        self._is_active = is_active
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

    def get_all_machines(self):
        query = "SELECT * FROM machines"
        return self._execute_query(query)

    def get_machine_by_id(self, machine_id):
        query = "SELECT * FROM machines WHERE machine_id = %s"
        return self._execute_query(query, (machine_id,), fetch_one=True)

    def create_machine(self):
        query = """
            INSERT INTO machines (
                machine_name, type, production_capacity, status, installation_date, last_maintenance, responsible, is_active
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            self._machine_name,
            self._type,
            self._production_capacity,
            self._status,
            self._installation_date,
            self._last_maintenance,
            self._responsible,
            self._is_active,
        )
        result = self._execute_query(query, values)
        if result is None:
            return {"message": "Error al crear máquina"}
        return {"message": "Máquina creada correctamente"}

    def update_machine(self, machine_id):
        query = """
            UPDATE machines
            SET machine_name=%s, type=%s, production_capacity=%s, status=%s, installation_date=%s, 
                last_maintenance=%s, responsible=%s, is_active=%s
            WHERE machine_id=%s
        """
        values = (
            self._machine_name,
            self._type,
            self._production_capacity,
            self._status,
            self._installation_date,
            self._last_maintenance,
            self._responsible,
            self._is_active,
            machine_id,
        )
        result = self._execute_query(query, values)
        if result is None:
            return {"message": "Error al actualizar máquina"}
        return {"message": "Máquina actualizada correctamente"}

    def delete_machine(self, machine_id):
        query = "DELETE FROM machines WHERE machine_id = %s"
        result = self._execute_query(query, (machine_id,))
        if result is None:
            return {"message": "Error al eliminar máquina"}
        return {"message": "Máquina eliminada correctamente"}
