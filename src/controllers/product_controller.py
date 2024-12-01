from src.models.product_model import ProductModel

class ProductController:
    def get_all_products(self):
        try:
            product_model = ProductModel()
            products = product_model.get_all_products()
            return products if products else {"message": "No se encontraron productos."}
        except Exception as e:
            print(f"Error al obtener productos: {e}")
            return {"message": "Error al obtener productos."}

    def create_product(self, product_name, description, production_cost, sale_price, stock, category, creation_date):
        try:
            if not all([product_name, production_cost, sale_price, creation_date]):
                return {"message": "Los campos obligatorios no pueden estar vacíos."}
            new_product = ProductModel(
                product_name=product_name,
                description=description,
                production_cost=production_cost,
                sale_price=sale_price,
                stock=stock,
                category=category,
                creation_date=creation_date
            )
            return new_product.create_product()
        except Exception as e:
            print(f"Error al crear producto: {e}")
            return {"message": "Error al crear producto."}

    def update_product(self, product_id, **kwargs):
        try:
            product_model = ProductModel()
            existing_product = product_model.get_product_by_id(product_id)
            if not existing_product:
                return {"message": "El producto no existe."}
            
            updated_product = ProductModel(
                product_name=kwargs.get("product_name", existing_product[1]),
                description=kwargs.get("description", existing_product[2]),
                production_cost=kwargs.get("production_cost", existing_product[3]),
                sale_price=kwargs.get("sale_price", existing_product[4]),
                stock=kwargs.get("stock", existing_product[5]),
                category=kwargs.get("category", existing_product[6]),
                creation_date=kwargs.get("creation_date", existing_product[7]),
                is_active=kwargs.get("is_active", existing_product[8])
            )
            return updated_product.update_product(product_id)
        except Exception as e:
            print(f"Error al actualizar producto con ID {product_id}: {e}")
            return {"message": "Error al actualizar producto."}

    def delete_product(self, product_id):
        try:
            product_model = ProductModel()
            existing_product = product_model.get_product_by_id(product_id)
            if not existing_product:
                return {"message": "El producto no existe."}
            return product_model.delete_product(product_id)
        except Exception as e:
            print(f"Error al eliminar producto con ID {product_id}: {e}")
            return {"message": "Error al eliminar producto."}
