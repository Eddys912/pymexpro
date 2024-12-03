from src.database.connection import DBConnection


class UserModel:
    def __init__(self):
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
            raise Exception(f"Error al ejecutar la consulta: {e}")
        finally:
            if cursor:
                cursor.close()
            self.db_connection.close()

    def get_all_users(self):
        query = """
            SELECT 
                CONCAT(first_name, ' ', last_name) AS full_name, 
                gender,
                username, 
                email, 
                CONCAT(SUBSTR(phone, 1, 3), '-', SUBSTR(phone, 4, 3), '-', SUBSTR(phone, 7, 4)) AS formatted_phone,
                role, 
                CASE 
                    WHEN is_active = 1 THEN 'Sí'
                    ELSE 'No'
                END AS is_active_status,
                TIMESTAMPDIFF(YEAR, birth_date, CURDATE()) AS age
            FROM users;

        """
        return self._execute_query(query)

    def get_user_by_id(self, user_id):
        query = "SELECT * FROM users WHERE id = %s"
        return self._execute_query(query, (user_id,), fetch_one=True)

    def get_user_by_email(self, email):
        query = "SELECT * FROM users WHERE email=%s"
        return self._execute_query(query, (email,), fetch_one=True)

    def get_user_by_username(self, username):
        query = "SELECT * FROM users WHERE username=%s"
        return self._execute_query(query, (username,), fetch_one=True)

    def create_user(self, user_data):
        query = """
            INSERT INTO users (first_name, last_name, gender, username, password, email, phone, role, birth_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            user_data["first_name"],
            user_data["last_name"],
            user_data["gender"],
            user_data["username"],
            user_data["password"],
            user_data["email"],
            user_data["phone"],
            user_data["role"],
            user_data["birth_date"],
        )

        return self._execute_query(query, values)

    def update_user(self, user_id, user_data):
        query = """
            UPDATE users
            SET first_name=%s, last_name=%s, gender=%s, username=%s, password=%s, email=%s, phone=%s, role=%s, is_active=%s, birth_date=%s WHERE id = %s
        """
        values = (
            user_data["first_name"],
            user_data["last_name"],
            user_data["gender"],
            user_data["username"],
            user_data["password"],
            user_data["email"],
            user_data["phone"],
            user_data["role"],
            user_data["is_active"],
            user_data["birth_date"],
            user_id,
        )
        return self._execute_query(query, values)

    def delete_user(self, user_id):
        query = "DELETE FROM users WHERE id = %s"
        return self._execute_query(query, (user_id,))
