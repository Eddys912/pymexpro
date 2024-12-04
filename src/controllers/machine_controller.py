from src.models.machine_model import MachineModel


class MachineController:
    def __init__(self):
        self.machine_model = MachineModel()

    def validate_machine_data(self, machine_data, is_update=False):
        required_fields = [
            "machine_name",
            "type",
            "installation_date",
            "status",
            "responsible",
        ]

        if not is_update:
            required_fields.append("production_capacity")

        missing_fields = [
            field
            for field in required_fields
            if field not in machine_data or not machine_data[field]
        ]
        if missing_fields:
            return {
                "success": False,
                "message": f"Faltan los campos obligatorios: {', '.join(missing_fields)}",
            }

        if "is_active" in machine_data and machine_data["is_active"] not in [0, 1]:
            return {
                "success": False,
                "message": "El campo 'Activo' debe ser 0 (Inactivo) o 1 (Activo).",
            }

        return {"success": True, "message": "Validación exitosa."}

    def create_machine(self, machine_data):
        validation = self.validate_machine_data(machine_data)
        if not validation["success"]:
            return validation
        try:
            self.machine_model.create_machine(machine_data)
            return {"success": True, "message": "Máquina creada correctamente."}
        except Exception as e:
            return {"success": False, "message": f"Error al crear máquina: {e}"}

    def update_machine(self, machine_id, machine_data):
        validation = self.validate_machine_data(machine_data, is_update=True)
        if not validation["success"]:
            return validation

        try:
            self.machine_model.update_machine(machine_id, machine_data)
            return {"success": True, "message": "Máquina actualizada correctamente."}
        except Exception as e:
            return {"success": False, "message": f"Error al actualizar máquina: {e}"}

    def delete_machine(self, machine_id):
        try:
            machine = self.machine_model.get_machine_by_id(machine_id)
            if machine is None:
                return {"success": False, "message": "Máquina no encontrada."}
            self.machine_model.delete_machine(machine_id)
            return {"success": True, "message": "Máquina eliminada correctamente."}
        except Exception as e:
            return {"success": False, "message": f"Error al eliminar máquina: {e}"}

    def get_machine_by_id(self, machine_id):
        try:
            machine = self.machine_model.get_machine_by_id(machine_id)
            if not machine:
                return {"success": False, "message": "Máquina no encontrada."}
            return {"success": True, "data": machine}
        except Exception as e:
            return {"success": False, "message": f"Error al obtener máquina: {e}"}

    def get_all_machines(self):
        try:
            machines = self.machine_model.get_all_machines()
            if not machines:
                return {"success": False, "message": "No se encontraron máquinas."}
            return {"success": True, "data": machines}
        except Exception as e:
            return {"success": False, "message": f"Error al obtener máquinas: {e}"}

    def get_filtered_machines(self, status=None, machine_type=None):
        try:
            machines = self.machine_model.get_filtered_machines(status, machine_type)
            if not machines:
                return {
                    "success": False,
                    "message": "No se encontraron máquinas con los filtros aplicados.",
                }
            return {"success": True, "data": machines}
        except Exception as e:
            return {"success": False, "message": f"Error al filtrar máquinas: {e}"}

    def get_search_machines(self, search_text):
        try:
            machines = self.machine_model.get_search_machines(search_text)
            if not machines:
                return {"success": False, "message": "No se encontraron máquinas."}
            return {"success": True, "data": machines}
        except Exception as e:
            return {"success": False, "message": f"Error al buscar máquinas: {e}"}
