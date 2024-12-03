import re
from datetime import datetime


class UserFormValidator:
    def validate_required_fields(data, required_fields):
        for field in required_fields:
            if not data.get(field):
                return False, f"El campo '{field}' no puede estar vacío."
        return True, "Todos los campos están completos."

    def validate_email(email):
        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_regex, email):
            return False, "El correo electrónico no es válido."
        return True, "Correo electrónico válido."

    def validate_phone(phone):
        if not phone.isdigit() or len(phone) != 10:
            return False, "El número de teléfono debe contener exactamente 10 dígitos."
        return True, "Número de teléfono válido."

    def validate_password(password):
        password_regex = r"^(?=.*[A-Z])(?=.*\d)(?=.*[a-zA-Z]).{8,}$"
        if not re.match(password_regex, password):
            return (
                False,
                "La contraseña debe tener al menos 8 caracteres, incluyendo una letra mayúscula y un número.",
            )
        return True, "Contraseña válida."

    def validate_birth_date(birth_date):
        try:
            birth_date_obj = datetime.strptime(birth_date, "%Y-%m-%d %H:%M:%S")
            age = (datetime.now() - birth_date_obj).days // 365
            if age < 18:
                return False, "El usuario debe ser mayor de 18 años."
        except ValueError:
            return False, "La fecha de nacimiento no es válida."
        return True, "Fecha de nacimiento válida."

    def validate_gender(gender):
        if gender not in ["Masculino", "Femenino"]:
            return False, "Seleccione un género válido."
        return True, "Género válido."
