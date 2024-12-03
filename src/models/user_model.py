from src.database.connection import DBConnection


class UserModel:
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

    def get_all_users(self):
        query = """
            SELECT 
                user_id,
                CONCAT(first_name, ' ', last_name) AS full_name,
                first_name,
                last_name,
                role, 
                username, 
                email, 
                CONCAT(SUBSTR(phone, 1, 3), '-', SUBSTR(phone, 4, 3), '-', SUBSTR(phone, 7, 4)) AS formatted_phone,
                phone,
                TIMESTAMPDIFF(YEAR, birth_date, CURDATE()) AS age,
                birth_date,
                gender,
                address,
                CASE 
                    WHEN is_active = 1 THEN 'Sí'
                    ELSE 'No'
                END AS is_active_status,
                is_active
            FROM users;
        """
        return self._execute_query(query)

    def get_user_by_id(self, user_id):
        query = "SELECT * FROM users WHERE user_id = %s"
        return self._execute_query(query, (user_id,), fetch_one=True)

    def create_user(self, user_data):
        query = """
            INSERT INTO users (first_name, last_name, gender, username, password, email, phone, role, birth_date, address)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
            user_data["address"],
        )
        return self._execute_query(query, values)

    def update_user(self, user_id, user_data):
        query = """
            UPDATE users
            SET first_name=%s, last_name=%s, gender=%s, username=%s, email=%s, phone=%s, role=%s, is_active=%s, birth_date=%s, address=%s
            WHERE user_id = %s
        """
        values = (
            user_data["first_name"],
            user_data["last_name"],
            user_data["gender"],
            user_data["username"],
            user_data["email"],
            user_data["phone"],
            user_data["role"],
            user_data["is_active"],
            user_data["birth_date"],
            user_data["address"],
            user_id,
        )
        return self._execute_query(query, values)

    def delete_user(self, user_id):
        query = "DELETE FROM users WHERE user_id = %s"
        return self._execute_query(query, (user_id,))

    def get_user_by_email(self, email):
        query = "SELECT * FROM users WHERE email=%s"
        return self._execute_query(query, (email,), fetch_one=True)

    def get_user_by_username(self, username):
        query = "SELECT * FROM users WHERE username=%s"
        return self._execute_query(query, (username,), fetch_one=True)

    def get_filtered_users(self, role=None, gender=None):
        query = """
            SELECT
                user_id,
                CONCAT(first_name, ' ', last_name) AS full_name,
                first_name, 
                last_name,
                role, 
                username, 
                email, 
                CONCAT(SUBSTR(phone, 1, 3), '-', SUBSTR(phone, 4, 3), '-', SUBSTR(phone, 7, 4)) AS formatted_phone,
                phone,
                TIMESTAMPDIFF(YEAR, birth_date, CURDATE()) AS age,
                birth_date,
                gender,
                address,
                CASE 
                    WHEN is_active = 1 THEN 'Sí'
                    ELSE 'No'
                END AS is_active_status,
                is_active
            FROM users
            WHERE (%s = 'Seleccionar rol' OR role = %s)
            AND (%s = 'Seleccionar sexo' OR gender = %s)
        """
        values = (
            role if role else "Seleccionar rol",
            role if role else None,
            gender if gender else "Seleccionar sexo",
            gender if gender else None,
        )
        return self._execute_query(query, values)

    def search_users(self, search_text):
        query = """
            SELECT
                user_id,
                CONCAT(first_name, ' ', last_name) AS full_name,
                first_name, 
                last_name,
                role, 
                username, 
                email, 
                CONCAT(SUBSTR(phone, 1, 3), '-', SUBSTR(phone, 4, 3), '-', SUBSTR(phone, 7, 4)) AS formatted_phone,
                phone,
                TIMESTAMPDIFF(YEAR, birth_date, CURDATE()) AS age,
                birth_date,
                gender,
                address,
                CASE 
                    WHEN is_active = 1 THEN 'Sí'
                    ELSE 'No'
                END AS is_active_status,
                is_active
            FROM users
            WHERE CONCAT(first_name, ' ', last_name) LIKE %s
            OR role LIKE %s
            OR username LIKE %s
            OR email LIKE %s
            OR phone LIKE %s
        """
        values = [f"%{search_text}%"] * 5
        return self._execute_query(query, values)
