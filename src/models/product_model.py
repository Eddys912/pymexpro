from src.database.connection import DBConnection


class ProductModel:
    def __init__(
        self,
        product_name="",
        description="",
        production_cost=0.0,
        sale_price=0.0,
        stock=0,
        category="",
        creation_date="",
        is_active=True,
    ):
        self._product_name = product_name
        self._description = description
        self._production_cost = production_cost
        self._sale_price = sale_price
        self._stock = stock
        self._category = category
        self._creation_date = creation_date
        self._is_active = is_active
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
            print(f"Error al ejecutar la consulta: {e}")
            return None
        finally:
            cursor.close()
            self.db_connection.close()

    def get_all_products(self):
        query = "SELECT * FROM products"
        return self._execute_query(query)

    def get_product_by_id(self, product_id):
        query = "SELECT * FROM products WHERE product_id = %s"
        return self._execute_query(query, (product_id,), fetch_one=True)

    def create_product(self):
        query = """
            INSERT INTO products (product_name, description, production_cost, sale_price, stock, category, creation_date, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            self._product_name,
            self._description,
            self._production_cost,
            self._sale_price,
            self._stock,
            self._category,
            self._creation_date,
            self._is_active,
        )
        return self._execute_query(query, values)

    def update_product(self, product_id):
        query = """
            UPDATE products
            SET product_name=%s, description=%s, production_cost=%s, sale_price=%s, stock=%s, category=%s, creation_date=%s, is_active=%s
            WHERE product_id=%s
        """
        values = (
            self._product_name,
            self._description,
            self._production_cost,
            self._sale_price,
            self._stock,
            self._category,
            self._creation_date,
            self._is_active,
            product_id,
        )
        return self._execute_query(query, values)

    def delete_product(self, product_id):
        query = "DELETE FROM products WHERE product_id = %s"
        return self._execute_query(query, (product_id,))
