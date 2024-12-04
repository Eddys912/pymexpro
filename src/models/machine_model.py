from src.database.connection import DBConnection


class MachineModel:
    def __init__(self):
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
            raise Exception(f"Error al ejecutar la consulta: {e}")
        finally:
            if cursor:
                cursor.close()
            self.db_connection.close()

    def get_all_machines(self):
        """
        Obtiene todas las máquinas de la base de datos.
        """
        query = """
            SELECT 
                machine_id,
                machine_name,
                type,
                production_capacity, 
                status, 
                installation_date,
                last_maintenance,
                responsible,
                CASE 
                    WHEN is_active = 1 THEN 'Sí'
                    ELSE 'No'
                END AS is_active_status,
                is_active
            FROM machines;
        """
        return self._execute_query(query)

    def get_machine_by_id(self, machine_id):
        query = "SELECT * FROM machines WHERE machine_id = %s"
        return self._execute_query(query, (machine_id,), fetch_one=True)

    def create_machine(self, machine_data):
        query = """
            INSERT INTO machines (
                machine_name, type, production_capacity, status, installation_date, last_maintenance, responsible
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            machine_data["machine_name"],
            machine_data["type"],
            machine_data["production_capacity"],
            machine_data["status"],
            machine_data["installation_date"],
            machine_data["last_maintenance"],
            machine_data["responsible"],
        )
        return self._execute_query(query, values)

    def update_machine(self, machine_id, machine_data):
        query = """
            UPDATE machines
            SET 
                machine_name = %s,
                type = %s,
                production_capacity = %s,
                status = %s,
                installation_date = %s,
                last_maintenance = %s,
                responsible = %s,
                is_active = %s
            WHERE machine_id = %s
        """
        values = (
            machine_data["machine_name"],
            machine_data["type"],
            machine_data["production_capacity"],
            machine_data["status"],
            machine_data["installation_date"],
            machine_data["last_maintenance"],
            machine_data["responsible"],
            machine_data["is_active"],
            machine_id,
        )
        return self._execute_query(query, values)

    def delete_machine(self, machine_id):
        query = "DELETE FROM machines WHERE machine_id = %s"
        return self._execute_query(query, (machine_id,))

    def get_filtered_machines(self, status=None, machine_type=None):
        query = """
            SELECT 
                machine_id,
                machine_name,
                type,
                production_capacity,
                status,
                installation_date,
                last_maintenance,
                responsible,
                CASE 
                    WHEN is_active = 1 THEN 'Sí'
                    ELSE 'No'
                END AS is_active_status,
                is_active
            FROM machines
            WHERE (%s = 'Seleccionar estatus' OR status = %s)
            AND (%s = 'Seleccionar tipo' OR type = %s)
        """
        values = (
            status if status else "Seleccionar estatus",
            status if status else None,
            machine_type if machine_type else "Seleccionar tipo",
            machine_type if machine_type else None,
        )
        return self._execute_query(query, values)

    def get_search_machines(self, search_text):
        query = """
            SELECT 
                machine_id,
                machine_name,
                type,
                production_capacity,
                status,
                installation_date,
                last_maintenance,
                responsible,
                CASE 
                    WHEN is_active = 1 THEN 'Sí'
                    ELSE 'No'
                END AS is_active_status,
                is_active
            FROM machines
            WHERE 
                machine_name LIKE %s
                OR type LIKE %s
                OR responsible LIKE %s
                OR status LIKE %s
        """
        values = [f"%{search_text}%"] * 4
        return self._execute_query(query, values)
