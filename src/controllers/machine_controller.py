from src.models.machine_model import MachineModel


class MachineController:
    def __init__(self):
        self.machine_model = MachineModel()

    def create_machine(self, machine_data):
        try:
            self.machine_model.create_user(machine_data)
            return {"success": True, "message": "Máquina creada correctamente."}
        except Exception as e:
            return {"success": False, "message": f"Error al crear máquina: {e}"}

    def update_machine(self, machine_id, machine_data):
        machine = self.machine_model.get_machine_by_id(machine_id)
        if not machine:
            return {"message": "La máquina no existe."}
        try:
            self.machine_model.update_machine(machine_id, machine_data)
            return {"success": True, "message": "Máquina actualizada correctamente."}
        except Exception as e:
            return {"success": False, "message": f"Error al actualizar máquina: {e}"}

    def delete_machine(self, machine_id):
        machine = self.machine_model.get_user_by_id(machine_id)
        if machine is None:
            return {
                "success": False,
                "message": f"Usuario con ID {machine_id} no encontrado.",
            }
        try:
            self.machine_model.delete_user(machine_id)
            return {"success": True, "message": "Máquina eliminada correctamente."}
        except Exception as e:
            return {"success": False, "message": f"Error al eliminar máquina: {e}"}

    def get_user_by_id(self, machine_id):
        try:
            user = self.machine_model.get_machine_by_id(machine_id)
            if user is None:
                return {
                    "success": False,
                    "message": f"Máquina con ID {machine_id} no encontrado.",
                }
            return {"success": True, "data": user}
        except Exception as e:
            return {"success": False, "message": f"Error al obtener máquina: {e}"}
        
    def get_all_machines(self):
        try:
            machine = self.machine_model.get_all_machines()
            if not machine:
                return {"success": False, "message": "No se encontraron máquinas."}
            return {"success": True, "data": machine}
        except Exception as e:
            return {"success": False, "message": f"Error al obtener máquinas: {e}"}
