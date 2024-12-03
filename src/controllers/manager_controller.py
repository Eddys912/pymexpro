from src.models.manager_model import ManagerModel


class ManagerController:
    def get_all_managers(self):
        try:
            manager_model = ManagerModel()
            managers = manager_model.get_all_managers()
            return managers if managers else {"message": "No se encontraron gerentes."}
        except Exception as e:
            print(f"Error al obtener gerentes: {e}")
            return {"message": "Error al obtener gerentes."}

    def create_manager(self, manager_id, shift, responsible_area):
        try:
            if not all([manager_id, shift, responsible_area]):
                return {"message": "Todos los campos son obligatorios."}
            new_manager = ManagerModel(
                manager_id=manager_id, shift=shift, responsible_area=responsible_area
            )
            return new_manager.create_manager()
        except Exception as e:
            print(f"Error al crear gerente: {e}")
            return {"message": "Error al crear gerente."}

    def update_manager(self, manager_id, **kwargs):
        try:
            manager_model = ManagerModel()
            existing_manager = manager_model.get_manager_by_id(manager_id)
            if not existing_manager:
                return {"message": "El gerente no existe."}

            updated_manager = ManagerModel(
                manager_id=manager_id,
                shift=kwargs.get("shift", existing_manager[1]),
                responsible_area=kwargs.get("responsible_area", existing_manager[2]),
            )
            return updated_manager.update_manager(manager_id)
        except Exception as e:
            print(f"Error al actualizar gerente con ID {manager_id}: {e}")
            return {"message": "Error al actualizar gerente."}

    def delete_manager(self, manager_id):
        try:
            manager_model = ManagerModel()
            existing_manager = manager_model.get_manager_by_id(manager_id)
            if not existing_manager:
                return {"message": "El gerente no existe."}
            return manager_model.delete_manager(manager_id)
        except Exception as e:
            print(f"Error al eliminar gerente con ID {manager_id}: {e}")
            return {"message": "Error al eliminar gerente."}
