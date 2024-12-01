from src.models.machine_model import MachineModel

class MachineController:
    def get_all_machines(self):
        try:
            machine_model = MachineModel()
            machines = machine_model.get_all_machines()
            return machines if machines else {"message": "No se encontraron máquinas."}
        except Exception as e:
            print(f"Error al obtener máquinas: {e}")
            return {"message": "Error al obtener máquinas."}

    def create_machine(self, machine_name, type, production_capacity, status, installation_date, last_maintenance, responsible):
        try:
            if not all([machine_name, type, installation_date]):
                return {"message": "Los campos obligatorios no pueden estar vacíos."}
            new_machine = MachineModel(
                machine_name=machine_name,
                type=type,
                production_capacity=production_capacity,
                status=status,
                installation_date=installation_date,
                last_maintenance=last_maintenance,
                responsible=responsible
            )
            return new_machine.create_machine()
        except Exception as e:
            print(f"Error al crear máquina: {e}")
            return {"message": "Error al crear máquina."}

    def update_machine(self, machine_id, **kwargs):
        try:
            machine_model = MachineModel()
            existing_machine = machine_model.get_machine_by_id(machine_id)
            if not existing_machine:
                return {"message": "La máquina no existe."}
            
            updated_machine = MachineModel(
                machine_name=kwargs.get("machine_name", existing_machine[1]),
                type=kwargs.get("type", existing_machine[2]),
                production_capacity=kwargs.get("production_capacity", existing_machine[3]),
                status=kwargs.get("status", existing_machine[4]),
                installation_date=kwargs.get("installation_date", existing_machine[5]),
                last_maintenance=kwargs.get("last_maintenance", existing_machine[6]),
                responsible=kwargs.get("responsible", existing_machine[7]),
                is_active=kwargs.get("is_active", existing_machine[8])
            )
            return updated_machine.update_machine(machine_id)
        except Exception as e:
            print(f"Error al actualizar máquina con ID {machine_id}: {e}")
            return {"message": "Error al actualizar máquina."}

    def delete_machine(self, machine_id):
        try:
            machine_model = MachineModel()
            existing_machine = machine_model.get_machine_by_id(machine_id)
            if not existing_machine:
                return {"message": "La máquina no existe."}
            return machine_model.delete_machine(machine_id)
        except Exception as e:
            print(f"Error al eliminar máquina con ID {machine_id}: {e}")
            return {"message": "Error al eliminar máquina."}
