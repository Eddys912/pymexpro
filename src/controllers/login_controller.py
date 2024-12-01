from src.models.user_model import UserModel
from src.database.connection import DBConnection


class LoginController:
    def authenticate_user(self, user: UserModel):
        cursor = None
        db = None
        try:
            db = DBConnection().connection()
            cursor = db.cursor()
            if user._username:
                query = "SELECT * FROM users WHERE username=%s AND password=%s"
                values = (user._username, user._password)
            elif user._email:
                query = "SELECT * FROM users WHERE email=%s AND password=%s"
                values = (user._email, user._password)
            cursor.execute(query, values)
            row = cursor.fetchone()
            if row:
                return UserModel(username=row[4], email=row[8], password=row[7])
            return {"message": "Credenciales inválidas."}
        except Exception as e:
            print(f"Error en login: {e}")
            return {"message": "No se puede acceder al sistema, intentarlo más tarde."}
        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()
