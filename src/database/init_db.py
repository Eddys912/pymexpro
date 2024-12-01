from connection import DBConnection
import create_tables as ct


def create_tables(connection):
    ct.drop_tables(connection)
    ct.create_table_users(connection)
    ct.create_table_managers(connection)
    ct.create_table_products(connection)
    ct.create_table_machines(connection)
    ct.create_table_production_reports(connection)
    ct.create_table_inventory(connection)


def insert_data_from_file(connection, file_path, table_name, columns):
    cursor = connection.cursor()
    try:
        with open(file_path, "r", encoding="utf8") as file:
            for line in file:
                values = line.strip().split(",")

                values = [
                    1 if v.lower() == "true" else 0 if v.lower() == "false" else v
                    for v in values
                ]

                if len(values) != len(columns):
                    raise ValueError(
                        f"Cantidad de valores ({len(values)}) no coincide con las columnas ({len(columns)})"
                    )

                placeholders = ", ".join(["%s"] * len(columns))
                query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
                cursor.execute(query, values)
        connection.commit()
        print(f"Datos insertados correctamente en la tabla '{table_name}'.")
    except Exception as e:
        print(f"Error al insertar datos en la tabla '{table_name}': {e}")
    finally:
        cursor.close()


if __name__ == "__main__":
    db = DBConnection()
    connection = db.connection()

    columns_user = [
        "user_id",
        "first_name",
        "last_name",
        "gender",
        "username",
        "password",
        "email",
        "phone",
        "role",
        "is_active",
        "birth_date",
        "registration_date",
    ]
    columns_products = [
        "product_id",
        "product_name",
        "description",
        "production_cost",
        "sale_price",
        "stock",
        "category",
        "creation_date",
        "is_active",
    ]
    columns_machine = [
        "machine_id",
        "machine_name",
        "type",
        "production_capacity",
        "status",
        "installation_date",
        "last_maintenance",
        "responsible",
        "is_active",
    ]
    columns_manager = [
        "manager_id",
        "shift",
        "responsible_area",
        "registration_date",
    ]

    if connection:
        create_tables(connection)
        insert_data_from_file(
            connection, "src/database/data/users.txt", "users", columns_user
        )
        insert_data_from_file(
            connection, "src/database/data/managers.txt", "managers", columns_manager
        )
        insert_data_from_file(
            connection, "src/database/data/products.txt", "products", columns_products
        )
        insert_data_from_file(
            connection, "src/database/data/machines.txt", "machines", columns_machine
        )
        db.close()
