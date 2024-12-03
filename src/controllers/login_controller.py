from src.models.user_model import UserModel


class LoginController:
    def __init__(self):
        self.user_model = UserModel()

    def authenticate_user(self, credentials_data):
        try:
            if "@" in credentials_data["username_or_email"]:
                user = self.user_model.get_user_by_email(
                    credentials_data["username_or_email"]
                )
            else:
                user = self.user_model.get_user_by_username(
                    credentials_data["username_or_email"]
                )
            if not user:
                return {"success": False, "message": "Usuario o correo no encontrado."}

            if user["password"] != credentials_data["password"]:
                return {"success": False, "message": "Contraseña incorrecta."}

            return {"success": True, "message": "Autenticación exitosa.", "user": user}

        except Exception as e:
            return {"success": False, "message": f"Error al autenticar usuario: {e}"}
