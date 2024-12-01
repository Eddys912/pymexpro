from src.database.connection import DBConnection


class UserModel:
    def __init__(
        self,
        first_name="",
        last_name="",
        gender="",
        username="",
        password="",
        email="",
        phone="",
        role="",
        is_active="True",
        birth_date="",
        registration_date="",
    ):
        self._first_name = first_name
        self._last_name = last_name
        self._gender = gender
        self._username = username
        self._password = password
        self._email = email
        self._phone = phone
        self._role = role
        self._is_active = is_active
        self._birth_date = birth_date
        self._registration_date = registration_date
        self.db_connection = DBConnection()

    def _execute_query(self, query, params=None, fetch_one=False):
        try:
            conn = self.db_connection.connection()
            cursor = conn.cursor()
            cursor.execute(query, params)
            if fetch_one:
                result = cursor.fetchone()
            else:
                result = cursor.fetchall()
            conn.commit()
            return result
        except Exception as e:
            print(f"Error al ejecutar la consulta: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            self.db_connection.close()

    def get_all_users(self):
        query = """
            SELECT 
                CONCAT(first_name, ' ', last_name) AS full_name, 
                CASE 
                    WHEN gender = 'M' THEN 'Masculino' 
                    WHEN gender = 'F' THEN 'Femenino' 
                    ELSE 'Otro' 
                END AS gender,
                username, 
                email, 
                phone, 
                role, 
                is_active, 
                TIMESTAMPDIFF(YEAR, birth_date, CURDATE()) AS age
            FROM users
        """
        users = self._execute_query(query)
        if users is None:
            return {"message": "Error al obtener los usuarios"}
        return users

    def get_user_by_id(self, user_id):
        query = "SELECT * FROM users WHERE id = %s"
        user = self._execute_query(query, (user_id,), fetch_one=True)
        if user is None:
            return {"message": f"Usuario con ID {user_id} no encontrado"}
        return user

    def create_user(self):
        query = """
            INSERT INTO users (first_name, last_name, gender, username, password, email, phone, role, is_active, birth_date, registration_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            self._first_name,
            self._last_name,
            self._gender,
            self._username,
            self._password,
            self._email,
            self._phone,
            self._role,
            self._is_active,
            self._birth_date,
            self._registration_date,
        )
        result = self._execute_query(query, values)
        if result is None:
            return {"message": "Error al crear usuario"}
        return {"message": "Usuario creado correctamente"}

    def update_user(self, user_id):
        user = self.get_user_by_id(user_id)
        if "message" in user:
            return user
        query = """
            UPDATE users
            SET first_name=%s, last_name=%s, gender=%s, username=%s, password=%s, email=%s, phone=%s, role=%s, is_active=%s, birth_date=%s, registration_date=%s
            WHERE id = %s
        """
        values = (
            self._first_name,
            self._last_name,
            self._gender,
            self._username,
            self._password,
            self._email,
            self._phone,
            self._role,
            self._is_active,
            self._birth_date,
            self._registration_date,
            user_id,
        )
        result = self._execute_query(query, values)
        if result is None:
            return {"message": "Error al actualizar usuario"}
        return {"message": "Usuario actualizado correctamente"}

    def delete_user(self, user_id):
        user = self.get_user_by_id(user_id)
        if "message" in user:
            return user

        query = "DELETE FROM users WHERE id = %s"
        result = self._execute_query(query, (user_id,))
        if result is None:
            return {"message": "Error al eliminar usuario"}
        return {"message": "Usuario eliminado correctamente"}
