from src.models.user_model import UserModel
from src.utils.user_form_validators import UserFormValidator as UFV


class UserController:
    def __init__(self):
        self.user_model = UserModel()

    def validate_user_data(self, user_data, is_update=False):
        required_fields = [
            "first_name",
            "last_name",
            "gender",
            "username",
            "email",
            "phone",
            "role",
            "birth_date",
            "address",
        ]

        if not is_update:
            required_fields.append("password")

        is_valid, message = UFV.validate_required_fields(user_data, required_fields)
        if not is_valid:
            return {"success": False, "message": message}

        if is_update and (
            "is_active" not in user_data or user_data["is_active"] not in [0, 1]
        ):
            return {
                "success": False,
                "message": "El campo 'Estatus' debe ser 'Activo' o 'Inactivo'.",
            }

        existing_user = self.user_model.get_user_by_email(user_data["email"])
        if existing_user and (
            not is_update or existing_user["user_id"] != user_data.get("user_id")
        ):
            return {
                "success": False,
                "message": "El correo electrónico ya está en uso.",
            }

        existing_username = self.user_model.get_user_by_username(user_data["username"])
        if existing_username and (
            not is_update or existing_username["user_id"] != user_data.get("user_id")
        ):
            return {"success": False, "message": "El nombre de usuario ya está en uso."}

        validators = [
            (UFV.validate_email, user_data["email"]),
            (UFV.validate_phone, user_data["phone"]),
            (UFV.validate_gender, user_data["gender"]),
            (UFV.validate_birth_date, user_data["birth_date"]),
        ]

        if not is_update or "password" in user_data and user_data["password"].strip():
            validators.append((UFV.validate_password, user_data["password"]))

        for validator, value in validators:
            is_valid, message = validator(value)
            if not is_valid:
                return {"success": False, "message": message}

        return {"success": True, "message": "Validación exitosa."}

    def create_user(self, user_data):
        validation = self.validate_user_data(user_data)
        if not validation["success"]:
            return validation
        try:
            self.user_model.create_user(user_data)
            return {"success": True, "message": "Usuario creado correctamente."}
        except Exception as e:
            return {"success": False, "message": f"Error al crear usuario: {e}"}

    def update_user(self, user_id, user_data):
        validation = self.validate_user_data(user_data, is_update=True)
        if not validation["success"]:
            return validation

        try:
            self.user_model.update_user(user_id, user_data)
            return {"success": True, "message": "Usuario actualizado correctamente."}
        except Exception as e:
            return {"success": False, "message": f"Error al actualizar usuario: {e}"}

    def delete_user(self, user_id):
        user = self.user_model.get_user_by_id(user_id)
        if user is None:
            return {
                "success": False,
                "message": f"Usuario con ID {user_id} no encontrado.",
            }
        try:
            self.user_model.delete_user(user_id)
            return {"success": True, "message": "Usuario eliminado correctamente."}
        except Exception as e:
            return {"success": False, "message": f"Error al eliminar usuario: {e}"}

    def get_user_by_id(self, user_id):
        try:
            user = self.user_model.get_user_by_id(user_id)
            if user is None:
                return {
                    "success": False,
                    "message": f"Usuario con ID {user_id} no encontrado.",
                }
            return {"success": True, "data": user}
        except Exception as e:
            return {"success": False, "message": f"Error al obtener usuario: {e}"}

    def get_all_users(self):
        try:
            users = self.user_model.get_all_users()
            if not users:
                return {"success": False, "message": "No se encontraron usuarios."}
            return {"success": True, "data": users}
        except Exception as e:
            return {"success": False, "message": f"Error al obtener usuarios: {e}"}

    def get_filtered_users(self, role=None, gender=None):
        try:
            users = self.user_model.get_filtered_users(role, gender)
            if not users:
                return {
                    "success": False,
                    "message": "No se encontraron usuarios con los filtros aplicados.",
                }
            return {"success": True, "data": users}
        except Exception as e:
            return {"success": False, "message": f"Error al filtrar usuarios: {e}"}

    def get_search_users(self, search_text):
        try:
            users = self.user_model.search_users(search_text)
            if not users:
                return {"success": False, "message": "No se encontraron usuarios."}
            return {"success": True, "data": users}
        except Exception as e:
            return {"success": False, "message": f"Error al buscar usuarios: {e}"}
